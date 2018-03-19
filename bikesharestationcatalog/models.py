from django.db import models


class Station(models.Model):
    """Based on the data from https://tor.publicbikesystem.net/ube/gbfs/v1/en/station_information"""
    id = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    capacity = models.PositiveSmallIntegerField()
