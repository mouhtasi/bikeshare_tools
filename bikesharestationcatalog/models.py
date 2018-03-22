from django.db import models
import os
import hashlib


class Station(models.Model):
    """Based on the data from https://tor.publicbikesystem.net/ube/gbfs/v1/en/station_information"""
    id = models.PositiveSmallIntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    capacity = models.PositiveSmallIntegerField()
    num_bikes_available = models.PositiveSmallIntegerField()
    num_docks_available = models.PositiveSmallIntegerField()


def hash_image(instance, filename):
    instance.image.open()
    contents = instance.image.read()
    fname, ext = os.path.splitext(filename)

    return 'image/{}{}'.format(hashlib.sha1(contents).hexdigest(), ext)
# TODO: figure out how to overwrite files with the same name


class StationImage(models.Model):
    station = models.ForeignKey('Station', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=hash_image)
    date = models.DateField(auto_now_add=True)
