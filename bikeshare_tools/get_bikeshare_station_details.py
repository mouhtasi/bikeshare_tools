import os.path
import requests
import json
import time
import pickle

current_dir = os.path.dirname(os.path.abspath(__file__))
filepath = os.path.join(current_dir, 'data_with_capacity.pickle')

response = requests.get('https://tor.publicbikesystem.net/ube/gbfs/v1/en/station_information')
station_data = json.loads(response.content)['data']['stations']

response = requests.get('https://tor.publicbikesystem.net/ube/gbfs/v1/en/station_status')
status_data = json.loads(response.content)['data']['stations']

t = time.time()

stations = []
if os.path.isfile(filepath):
    with open(filepath, 'rb') as f:
        stations = pickle.load(f)

station_status_merged = {}
for station in station_data + status_data:
    key = station['station_id']
    if key not in station_status_merged:
        station_status_merged[key] = {}
    station_status_merged[key].update(station)
    del station_status_merged[key]['station_id']

for id, s in station_status_merged.items():
    if s['last_reported']:
        stations.append({'timestamp': t, 'name': s['name'], 'lat': s['lat'], 'lon': s['lon'],
                         'bikes_available': s['num_bikes_available'], 'capacity': s['capacity']})


with open(filepath, 'wb') as f:
    pickle.dump(stations, f, pickle.HIGHEST_PROTOCOL)
