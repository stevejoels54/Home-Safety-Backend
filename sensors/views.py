from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view
from rest_framework.response import Response
from sensors.models import Sensor, SensorData, Location
from sensors.serializers import SensorSerializer, SensorDataSerializer
from rest_framework import status
import json


# get most recently added Sensor Data from database and return it as JSON_RESPONSE


def getSensorData(request):
    sensorData = SensorData.objects.all().order_by(
        '-id')[0]  # get most recently added Sensor Database
    serializer = SensorDataSerializer(
        sensorData, many=False)  # serialize Sensor Data
    # return Sensor Data as JSON_RESPONSE
    return JsonResponse({'sensorData': serializer.data})

# get all Sensor Data from database and return it as JSON_RESPONSE


def getSensorDataList(request):
    sensorData = SensorData.objects.all().order_by('-id')
    serializer = SensorDataSerializer(sensorData, many=True)
    return JsonResponse({'sensorData': serializer.data})


# function to post sensor data to database

@require_http_methods(["POST"])
def postSensorData(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except:
            data = {}
        if data:
            try:
                lpg = data['lpg']
                smoke = data['smoke']
                temperature = data['temperature']
                location_id = data['location_id']
                sensorData = SensorData(
                    lpg=lpg, smoke=smoke, temperature=temperature)
                sensorData.save()
                return JsonResponse({'message': "Sensor Data Saved"}, status=201)
            except:
                return JsonResponse({'message': "Invalid Data"}, status=401)

    return JsonResponse({'message': "Invalid Data"}, status=401)


# Register a new place
def createLocation(request):
    if request.method == "POST":
        try:
            placeDetails = json.loads(request.body)
        except:
            placeDetails = {}

        if Location.objects.get(place_name=placeDetails['place_name']):
            return JsonResponse({'message': 'Location already exists.'}, status=401)
        else:
            try:
                x_coordinate = placeDetails['x_coordinate']
                y_coordinate = placeDetails['y_coordinate']
                place_name = placeDetails['place_name']
                location = Location(
                    x_coordinate=x_coordinate, y_coordinate=y_coordinate, place_name=place_name)
                location.save()
                return JsonResponse({'message': "Location Saved."}, status=201)
            except:
                return JsonResponse({'message': "Invalid location data."}, status=401)
    return JsonResponse({'message': "Invalid Data"}, status=401)


# Get location details
def getLocations(request):
    try:
        places = Location.objects.all()
        return JsonResponse({'Locations': places}, status=201)
    except:
        return JsonResponse({'message': 'First add new locations.'})


# get sensor data trend for the last 1 hour in 10 minutes intervals
def getValuesTrend(request):
    sensorData = SensorData.objects.all().order_by('-id')[0]
    value_id = sensorData.id
    if (value_id > 720):
        start = value_id - 720
        values = []
        # get data id in intervals of 120 (every 10mins)
        for i in range(start, start+721, 120):
            values.append(SensorData.objects.get(id=i))
            serializer = SensorDataSerializer(values, many=True)
        return JsonResponse({'sensorData': serializer.data}, status=200)
    else:
        values = []
        for i in range(1, value_id+1, 120):  # get data id in intervals of 120 (every 10mins)
            values.append(SensorData.objects.get(id=i))
            serializer = SensorDataSerializer(values, many=True)
        return JsonResponse({'sensorData': serializer.data}, status=200)
