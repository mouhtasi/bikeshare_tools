from django.shortcuts import render
import folium


def index(request):
    m = folium.Map(location=[43.66093,-79.3880384], zoom_start=13.5)

    context = {'map_file': m._repr_html_()}
    return render(request, 'heatmap/index.html', context)
