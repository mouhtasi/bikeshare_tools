from django.shortcuts import render
from bikesharestationcatalog.models import Station, StationImage
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import QuerySet
from bikesharestationcatalog.forms import ImageForm


def serialize_geojson(model_queryset):
    geo = {'type': 'FeatureCollection', 'features': []}

    if not isinstance(model_queryset, QuerySet):
        model_queryset = [model_queryset]

    for model in model_queryset:
        geo['features'].append({
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [model.longitude, model.latitude]
            },
            'properties': {
                'id': model.id,
                'name': model.name
            }
        })

    return json.dumps(geo, cls=DjangoJSONEncoder)


def catalog_home(request):
    geojson = serialize_geojson(Station.objects.all())
    return render(request, 'bikesharestationcatalog/catalog.html', {'geojson': geojson})


def station_details(request, s_id):
    station = Station.objects.get(id=s_id)
    images = StationImage.objects.filter(station=station)

    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            newimg = StationImage(station=station, image=request.FILES['imgfile'])
            newimg.save()
    else:
        form = ImageForm()

    geojson = serialize_geojson(station)

    return render(request, 'bikesharestationcatalog/station_details.html', {'station': station, 'geojson': geojson,
                                                                            'form': form, 'images': images})
