from rest_framework import serializers
from sensors.models import Sensor, SensorData, Location


class SensorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sensor
        fields = ['sensor_id', 'sensor_name', 'sensor_value', 'sensor_unit',
                  'sensor_status', 'sensor_location', 'sensor_description', 'sensor_timestamp']


class SensorDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = SensorData
        fields = ['id', 'lpg', 'smoke', 'temperature',
                  'data_timestamp', 'location_id']


class LocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = ['id', 'x_coordinate', 'y_coordinate', 'place_name']


# validate the data before saving it to the database


def validate(self, data):
    if data['lpg'] < 0:
        raise serializers.ValidationError("LPG value cannot be negative")
    if data['smoke'] < 0:
        raise serializers.ValidationError("Smoke value cannot be negative")
    if data['temperature'] < 0:
        raise serializers.ValidationError(
            "Temperature value cannot be negative")
    return data
