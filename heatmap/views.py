from django.shortcuts import render
from .forms import BikeShareHtmlInput
import folium
from folium import plugins
import os.path
import time
import requests
import json
from bs4 import BeautifulSoup
import pickle
from django.http import HttpResponse


def index(request):
    return render(request, 'heatmap/index.html')


def personal_heatmap(request):
    context = {}
    current_dir = os.path.dirname(os.path.abspath(__file__))

    if not request.session.get('has_session'):  # make a session so we can keep user's work isolated
        request.session['has_session'] = True

    if request.method == 'POST':
        form = BikeShareHtmlInput(request.POST)
        if form.is_valid() and form.cleaned_data['html_paste']:
            user_entered_html = form.cleaned_data['html_paste']
            map = generate_map(user_entered_html)
            map.save(os.path.join(current_dir, '../heatmap/templates/heatmap/generated_map{}.html'.format(
                request.session.session_key)))
            context['iframe_url'] = 'generated_trip_map_endpoint'
        else:
            check_and_generate_sample_map()
            context['iframe_url'] = 'sample_trip_map_endpoint'
    else:
        form = BikeShareHtmlInput()
        check_and_generate_sample_map()
        context['iframe_url'] = 'sample_trip_map_endpoint'

    context['form'] = form

    return render(request, 'heatmap/personal_heatmap.html', context)


# create a sample map if it doesn't already exist
def check_and_generate_sample_map():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sample_map_path = os.path.join(current_dir, '../heatmap/templates/heatmap/sample_map.html')
    if not os.path.isfile(sample_map_path):
        sample_data_path = os.path.join(current_dir, 'sample_data/sample_data')
        with open(sample_data_path) as f:
            sample_html = f.read()
        m = generate_map(sample_html)
        with open(os.path.join(current_dir, 'sample_derp.html'), 'w') as f:
            f.write(m._repr_html_())
        m.save(sample_map_path)


# generate and return the map built using the trip html data
def generate_map(html):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    api_file_path = os.path.join(current_dir, 'bikeshare_api/station_information')
    check_and_update_api_file(api_file_path)

    # read the station information and get their name and coordinates
    with open(api_file_path) as f:
        data = json.load(f)
    station_data = data['data']['stations']
    station_lat_long = {}
    for station in station_data:
        station_lat_long[station['name']] = {'lat': station['lat'], 'lon': station['lon']}

    # parse the html to get the trip data
    soup = BeautifulSoup(html, 'html.parser')
    rows = soup.find('div', class_='table-responsive').table.tbody.findAll('tr')
    user_trips = []
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        user_trips.append([ele for ele in cols if ele])  # Get rid of empty values

    # go through the trips and keep count of often each was used
    station_trip_count = {}
    for trip in user_trips:
        station_from = trip[1]
        station_to = trip[3]
        station_trip_count[station_from] = station_trip_count.get(station_from, 0) + 1
        station_trip_count[station_to] = station_trip_count.get(station_to, 0) + 1

    m = folium.Map(location=[43.66093, -79.3880384], zoom_start=13, tiles='Stamen Toner')

    # build the heatmap data using the coordinates and trip count
    # meanwhile also generate the points on the map
    heatmap_values = []
    for key, value in station_trip_count.items():  # convert name:count to [lat, lon, count]
        lat = station_lat_long[key]['lat']
        lon = station_lat_long[key]['lon']
        heatmap_values.append([lat, lon, value])
        folium.Circle([lat, lon], radius=4, fill=True, popup='{}<br>Count: {}'.format(key, value)).add_to(m)

    m.add_child(plugins.HeatMap(heatmap_values, radius=15, blur=20))

    return m


def sample_trip_map_endpoint(request):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    map_file = os.path.join(current_dir, '../heatmap/templates/heatmap/sample_map.html')
    with open(map_file, 'r') as f:
        m = f.read()
    return HttpResponse(m)


def generated_trip_map_endpoint(request):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    map_file = os.path.join(current_dir, '../heatmap/templates/heatmap/generated_map{}.html'.format(
        request.session.session_key))
    with open(map_file, 'r') as f:
        m = f.read()
    os.remove(map_file)
    return HttpResponse(m)


# if the station_information file is older than 5 minutes, update it from the API
def check_and_update_api_file(filepath):
    if time.time() - os.path.getmtime(filepath) > (5 * 60):
        response = requests.get('https://tor.publicbikesystem.net/ube/gbfs/v1/en/station_information')
        with open(filepath, 'wb') as f:
            f.write(response.content)


"""Below is code for the animated system heatmap page"""


def system_heatmap(request):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    map_file_1 = os.path.join(current_dir, '../heatmap/templates/heatmap/m1.html')
    map_file_2 = os.path.join(current_dir, '../heatmap/templates/heatmap/m2.html')

    if not os.path.isfile(map_file_1) and not os.path.isfile(map_file_2):  # we don't need to do the work again
        filepath = os.path.join(current_dir, '../bikeshare_tools/filtered_data_with_capacity.pickle')

        with open(filepath, 'rb') as f:
            stations_data = pickle.load(f)

        create_and_save_global_maps(stations_data)

    return render(request, 'heatmap/system_heatmap.html')


def create_and_save_global_maps(stations_data):
    m1 = folium.Map(location=[43.6531661,-79.394812], zoom_start=13, tiles='Stamen Toner', prefer_canvas=True,
                    detect_retina=True)
    m2 = folium.Map(location=[43.6531661,-79.394812], zoom_start=13, tiles='Stamen Toner', prefer_canvas=True,
                    detect_retina=True)
    times = []  # [time, time, time, ...]
    stations = []  # [[[lat, lon, w], [lat, lon, w], ...], [[lat, lon, w], [lat, lon, w], ...]]
    stations_by_capacity = []
    for time_station in stations_data:
        if time_station['bikes_available'] == 0:
            time_station['bikes_available'] = 1
        station = [time_station['lat'], time_station['lon'], time_station['bikes_available']]
        station_by_capacity = [time_station['lat'], time_station['lon'],
                               time_station['bikes_available'] / time_station['capacity']]

        unix_timestamp = time_station['timestamp']
        unix_timestamp -= 60 * 60 * 5  # UTC to EST/EDT -5h
        timestamp = time.strftime('%H:%M', time.localtime(unix_timestamp))
        if len(times) == 0 or timestamp != times[-1]:
            times.append(timestamp)
            stations.append([station])
            stations_by_capacity.append([station_by_capacity])
        else:
            stations[-1].append(station)  # outer lists need to correspond with timestamps index
            stations_by_capacity[-1].append(station_by_capacity)

    m1.add_child(plugins.HeatMapWithTime(stations, times, radius=30, use_local_extrema=True))
    m2.add_child(plugins.HeatMapWithTime(stations_by_capacity, times, radius=30))

    current_dir = os.path.dirname(os.path.abspath(__file__))
    map_file_1 = os.path.join(current_dir, '../heatmap/templates/heatmap/m1.html')
    map_file_2 = os.path.join(current_dir, '../heatmap/templates/heatmap/m2.html')
    m1.save(map_file_1)
    m2.save(map_file_2)


def global_heatmap_by_number_of_bikes(request):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    map_file = os.path.join(current_dir, '../heatmap/templates/heatmap/m1.html')
    with open(map_file, 'r') as f:
        m = f.read()
    return HttpResponse(m)


def global_heatmap_by_station_capacity(request):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    map_file = os.path.join(current_dir, '../heatmap/templates/heatmap/m2.html')
    with open(map_file, 'r') as f:
        m = f.read()
    return HttpResponse(m)
