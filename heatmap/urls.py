from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('personal_heatmap/', views.personal_heatmap, name='personal_heatmap'),
    path('sample_trip_map_endpoint/', views.sample_trip_map_endpoint, name='sample_trip_map_endpoint'),
    path('generated_trip_map_endpoint/', views.generated_trip_map_endpoint, name='generated_trip_map_endpoint'),
    path('system_heatmap/', views.system_heatmap, name='system_heatmap'),
    path('global_heatmap_by_number_of_bikes/', views.global_heatmap_by_number_of_bikes,
         name='global_heatmap_by_number_of_bikes'),
    path('global_heatmap_by_station_capacity/', views.global_heatmap_by_station_capacity,
         name='global_heatmap_by_station_capacity'),
]