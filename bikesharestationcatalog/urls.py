from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.catalog_home, name='station_catalog_home'),
    path('station_details/<int:s_id>/', views.station_details, name='station_details'),
    path('admin/', admin.site.urls)
]
