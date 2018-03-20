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

        station_data = json.loads(response.content)['data']['stations']

        num_updated = 0
        num_created = 0
        for station in station_data:
            s, created = Station.objects.update_or_create(id=station['station_id'],
                                                          defaults={'name': station['name'],
                                                                    'longitude': station['lon'],
                                                                    'latitude': station['lat'],
                                                                    'capacity': station['capacity']})
            if created:
                num_created += 1
            else:
                num_updated += 1

        self.stdout.write(self.style.SUCCESS('Stations updated. {} updated. {} created'.format(num_updated,
                                                                                               num_created)))
