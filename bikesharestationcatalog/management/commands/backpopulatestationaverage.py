from django.core.management.base import BaseCommand, CommandError
from bikesharestationcatalog.models import Station, StationAverageLog
import pytz
from datetime import datetime, timedelta
import os.path
import pickle
import requests
import json


class Command(BaseCommand):
    help = 'Updates the Station table using historical data from a pickle file'

    db = {}  # a dict replacing the db

    def handle(self, *args, **options):
        # assume that stations already exist
        # if a station doesn't exist, ignore the data, no point in adding it now

        # some station names have changed
        STATION_SUBSTITUTIONS = {"Queen St E / Berkely St": "Queen St E / Berkeley St"}

        current_dir = os.path.dirname(os.path.abspath(__file__))
        data_filepath = os.path.join(current_dir, '../../../bikeshare_tools/bikeshare_api_data.pickle')

        response = requests.get('https://tor.publicbikesystem.net/ube/gbfs/v1/en/station_information')
        if response.status_code != requests.codes.ok:
            raise CommandError('Failed to access API')
        station_data = json.loads(response.content)['data']['stations']

        station_name_to_id = {station['name']: station['station_id'] for station in station_data}

        # save a dict of all the Station objects by id to save on queries
        stations_by_id = {station.id: station for station in Station.objects.all()}

        # load all the records
        historical_log = []
        if os.path.isfile(data_filepath):
            with open(data_filepath, 'rb') as f:
                historical_log = pickle.load(f)

        # loop through the records, format the time, get the station id, load the station object, then update the mean
        for record in historical_log:
            if record['capacity'] == 0:
                # sometimes a station has capacity of 0 for some reason. This is weird and breaks calculation so skip
                self.stdout.write(self.style.WARNING('Capacity is 0 for station {}'.format(record['name'])))
                continue

            unix_timestamp = record['timestamp']
            datetime_timestamp = datetime.fromtimestamp(unix_timestamp, pytz.timezone('America/Toronto'))
            datetime_timestamp = datetime_timestamp - timedelta(minutes=datetime_timestamp.minute % 5,
                                                                seconds=datetime_timestamp.second,
                                                                microseconds=datetime_timestamp.microsecond)  # round down to the nearest 5 minutes
            time = datetime_timestamp.strftime('%H:%M')
            day = datetime_timestamp.strftime('%A')
            station_id = station_name_to_id.get(record['name'], None)

            # the data saved station names instead of IDs so some names have changed
            if not station_id:
                # self.stdout.write(self.style.WARNING('"{}" not found, trying flipped version'.format(record['name'])))
                flipped_name = ' / '.join(record['name'].split(' / ')[::-1])
                station_id = station_name_to_id.get(flipped_name, None)

                if not station_id:
                    # self.stdout.write(self.style.WARNING(
                    #     '"{}", flipped version of "{}" was not found. Checking for hardcoded substitution'.format(
                    #         flipped_name, record['name'])))
                    station_id = station_name_to_id.get(STATION_SUBSTITUTIONS.get(record['name'], ''), None)
                    # self.stdout.write(STATION_SUBSTITUTIONS.get(record['name'], ''))

                    # if station_id:
                    # self.stdout.write(self.style.WARNING('Successfully substituted'))
                    # else:
                    # self.stdout.write(self.style.ERROR('"{}" was not found.'.format(record['name'])))

            station = stations_by_id[station_id]
            self.update_average_local(station, record['bikes_available'], record['capacity'], time, day)
        self.save_to_db(stations_by_id)

    def update_average_local(self, station, num_bikes_available, capacity, time, day):
        if station.id not in self.db.keys():
            self.db[station.id] = {}

        station_record = self.db[station.id]

        if day not in station_record.keys():
            station_record[day] = {'time_data': {}}

        if time not in station_record[day]['time_data'].keys():
            station_record[day]['time_data'][time] = {'mean': 0, 'count': 0}

        new_mean = (station_record[day]['time_data'][time]['mean'] * station_record[day]['time_data'][time]['count']
                    + num_bikes_available / capacity) / (station_record[day]['time_data'][time]['count'] + 1)

        station_record[day]['time_data'][time]['mean'] = round(new_mean, 2)
        station_record[day]['time_data'][time]['count'] += 1

        # self.stdout.write(
        #     'Day: {}, Time: {}, Count: {}, Mean: {}, Station: {}'.format(day, time,
        #                                                                  station_record[day]['time_data'][time]['count'],
        #                                                                  station_record[day]['time_data'][time]['mean'],
        #                                                                  station.name))

    def save_to_db(self, stations_by_id):
        ctr = 0
        for station_id, station_record in self.db.items():
            ctr += 1
            for day, station_record_day in station_record.items():
                station_average, created = StationAverageLog.objects.get_or_create(station=stations_by_id[station_id],
                                                                                   day_of_week=day, defaults={
                        'time_data': station_record_day['time_data']})
                station_average.save()
        print('{} station records saved'.format(ctr))
