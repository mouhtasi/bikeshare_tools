from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('heatmap/', include('heatmap.urls')),
    path('catalog/', include('bikesharestationcatalog.urls')),
]
