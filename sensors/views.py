from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view
from rest_framework.response import Response
from sensors.models import Sensor, SensorData
from sensors.serializers import SensorSerializer, SensorDataSerializer
from rest_framework import status
import json

# Create your views here.

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
                sensorData = SensorData(
                    lpg=lpg, smoke=smoke, temperature=temperature)
                sensorData.save()
                return JsonResponse({'message': "Sensor Data Saved"}, status=201)
            except:
                return JsonResponse({'message': "Invalid Data"}, status=401)

    return JsonResponse({'message': "Invalid Data"}, status=401)
