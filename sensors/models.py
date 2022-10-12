from django.db import models

# Create your models here.


class Sensor(models.Model):
    sensor_id = models.CharField(max_length=50)
    sensor_name = models.CharField(max_length=50)
    sensor_unit = models.CharField(max_length=50)
    sensor_status = models.CharField(max_length=50)
    sensor_location = models.CharField(max_length=500)
    sensor_description = models.CharField(max_length=1000)

    def __str__(self):
        return self.sensor_id


class Location(models.Model):
    x_coordinate = models.CharField(
        max_length=500, null=True, blank=True, default=None)
    y_coordinate = models.CharField(
        max_length=500, null=True, blank=True, default=None)
    place_name = models.CharField(
        max_length=500, null=True, blank=True, default=None)

    def __str__(self):
        return self.place_name


class SensorData(models.Model):
    lpg = models.FloatField(null=True, blank=True, default=None)
    smoke = models.FloatField(null=True, blank=True, default=None)
    temperature = models.FloatField(null=True, blank=True, default=None)
    location_id = models.IntegerField(null=True, blank=True, default=None)
    data_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.data_timestamp)
