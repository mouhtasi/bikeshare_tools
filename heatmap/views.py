from django.shortcuts import render
from .forms import BikeShareHtmlInput
import folium


def index(request):
    context = {'map': None}
    if request.method == 'POST':
        form = BikeShareHtmlInput(request.POST)
        m = folium.Map(location=[43.66093, -79.3880384], zoom_start=13.5)
        context['map'] = m._repr_html_()
    else:
        form = BikeShareHtmlInput()
    context['form'] = form
    return render(request, 'heatmap/index.html', context)
