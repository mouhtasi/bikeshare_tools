from django.core.management.base import BaseCommand, CommandError
from bikesharestationcatalog.models import Station, StationAverageLog
import requests
import json
import pytz
from datetime import datetime, timedelta


# TODO: Add a check to only update if data is changed


class Command(BaseCommand):
    help = 'Updates the Station table using API data'

    def handle(self, *args, **options):
        response = requests.get('https://tor.publicbikesystem.net/ube/gbfs/v1/en/station_information')
        if response.status_code != requests.codes.ok:
            raise CommandError('Failed to access API')

        station_information = json.loads(response.content)['data']['stations']

        response = requests.get('https://tor.publicbikesystem.net/ube/gbfs/v1/en/station_status')
        if response.status_code != requests.codes.ok:
            raise CommandError('Failed to access API')

        station_status = json.loads(response.content)['data']['stations']

        station_status_merged = {}
        for station in station_information + station_status:
            key = station['station_id']
            if key not in station_status_merged:
                station_status_merged[key] = {}
            station_status_merged[key].update(station)

        d = datetime.now(pytz.timezone('America/Toronto'))
        d = d - timedelta(minutes=d.minute % 5, seconds=d.second,
                          microseconds=d.microsecond)  # round down to the nearest 5 minutes
        time = d.strftime('%H:%M')
        day = d.strftime('%A')

        num_updated = 0
        num_created = 0
        num_ignored = 0
        for station in station_status_merged.values():
            if station['last_reported']:  # there are stations that have no data but exist in one of the api outputs
                s, created = Station.objects.update_or_create(id=station['station_id'],
                                                              defaults={'name': station['name'],
                                                                        'longitude': station['lon'],
                                                                        'latitude': station['lat'],
                                                                        'capacity': station['capacity'],
                                                                        'num_bikes_available': station[
                                                                            'num_bikes_available'],
                                                                        'num_docks_available': station[
                                                                            'num_docks_available']})
                if created:
                    num_created += 1
                else:
                    num_updated += 1

                self.update_average(s, station['num_bikes_available'], station['capacity'], time, day)
            else:
                num_ignored += 1

        self.stdout.write(self.style.SUCCESS('Stations updated. {} updated. {} created. {} ignored.'.format(num_updated,
                                                                                                            num_created,
                                                                                                            num_ignored
                                                                                                            )))

    def update_average(self, station, num_bikes_available, capacity, time, day):
        # check if the historical object exists
        # if not then the count is 1 and average is current value
        # else get the data, calculate the new average
        # save

        # time_data is {'00:05': {mean=1, count=1}, ...
        station_average, created = StationAverageLog.objects.get_or_create(station=station, day_of_week=day, defaults={
            'time_data': {time: {
                'mean': 0,
                'count': 0
            }}})

        if created:
            station_average.time_data[time]['mean'] = round(num_bikes_available / capacity, 2)
            station_average.time_data[time]['count'] = 1
        else:
            if time not in station_average.time_data.keys():
                station_average.time_data[time] = {'mean': 0, 'count': 0}
            # cumulative mean
            new_mean = (station_average.time_data[time]['mean'] * station_average.time_data[time]['count']
                        + num_bikes_available / capacity) / (station_average.time_data[time]['count'] + 1)
            station_average.time_data[time]['mean'] = round(new_mean, 2)
            station_average.time_data[time]['count'] += 1

        station_average.save()

        # self.stdout.write(
        #     'Day: {}, Time: {}, Count: {}, Mean: {}, Station: {}'.format(day, time,
        #                                                                  station_average.time_data[time]['count'],
        #                                                                  station_average.time_data[time]['mean'],
        #                                                                  station_average.station.name))
