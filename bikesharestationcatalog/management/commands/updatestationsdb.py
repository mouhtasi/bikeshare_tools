from django.core.management.base import BaseCommand, CommandError
from bikesharestationcatalog.models import Station
import requests
import json


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
            else:
                num_ignored += 1

        self.stdout.write(self.style.SUCCESS('Stations updated. {} updated. {} created. {} ignored.'.format(num_updated,
                                                                                                            num_created,
                                                                                                            num_ignored
                                                                                                            )))
