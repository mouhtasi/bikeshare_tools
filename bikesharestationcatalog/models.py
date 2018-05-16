from django.db import models
from django.contrib.postgres.fields import JSONField
import os
import hashlib
from django.conf import settings


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
    path = 'image/{}{}'.format(hashlib.sha1(contents).hexdigest(), ext)

    # Django will normally add a unique string to the end of a filename if it already exists
    # but we'd rather not have that since we're naming the files by hash
    # so delete the existing file so Django will use the plain file name
    # we'll end up with duplicate entries in the database but we can just check for count before deleting the image
    full_path = os.path.join(settings.MEDIA_ROOT, path)
    if os.path.exists(full_path):
        os.remove(full_path)

    return path


class StationImage(models.Model):
    station = models.ForeignKey('Station', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=hash_image)
    date = models.DateField(auto_now_add=True)


class StationAverageLog(models.Model):
    station = models.ForeignKey('Station', on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=10)
    time_data = JSONField()
