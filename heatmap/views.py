from django.shortcuts import render
from .forms import BikeShareHtmlInput
import folium
import os.path
import time
import requests
import json
from bs4 import BeautifulSoup


def index(request):
    context = {'map': None}
    if request.method == 'POST':
        form = BikeShareHtmlInput(request.POST)

        if form.is_valid():
            current_dir = os.path.dirname(os.path.abspath(__file__))
            api_file_path = os.path.join(current_dir, 'bikeshare_api/station_information')
            check_and_update_api_file(api_file_path)

            with open(api_file_path) as f:
                data = json.load(f)
            station_data = data['data']['stations']

            user_entered_html = form.cleaned_data['html_paste']
            soup = BeautifulSoup(user_entered_html, 'html.parser')
            rows = soup.find('div', class_='table-responsive').table.tbody.findAll('tr')
            user_trips = []
            for row in rows:
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                user_trips.append([ele for ele in cols if ele])  # Get rid of empty values

            station_trip_count = {}
            for trip in user_trips:
                station_from = trip[1]
                station_to = trip[3]
                station_trip_count[station_from] = station_trip_count.get(station_from, 0) + 1
                station_trip_count[station_to] = station_trip_count.get(station_to, 0) + 1

            m = folium.Map(location=[43.66093, -79.3880384], zoom_start=13.5, tiles='Stamen Toner')
            context['map'] = m._repr_html_()
    else:
        form = BikeShareHtmlInput()
    context['form'] = form
    return render(request, 'heatmap/index.html', context)


def check_and_update_api_file(filepath):
    if time.time() - os.path.getmtime(filepath) > (5 * 60):
        response = requests.get('https://tor.publicbikesystem.net/ube/gbfs/v1/en/station_information')
        with open(filepath, 'wb') as f:
            f.write(response.content)
