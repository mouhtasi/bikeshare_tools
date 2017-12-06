from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('heatmapwithtime/', views.global_heatmap),
    path('global_heatmap_by_number_of_bikes/', views.global_heatmap_by_number_of_bikes,
         name='global_heatmap_by_number_of_bikes'),
    path('global_heatmap_by_station_capacity/', views.global_heatmap_by_station_capacity,
         name='global_heatmap_by_station_capacity'),
]