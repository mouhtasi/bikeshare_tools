from django.urls import path
from . import views

urlpatterns = [
    path('', views.catalog_home, name='home'),
    path('station_details/<int:s_id>/', views.station_details, name='station_details'),
]
