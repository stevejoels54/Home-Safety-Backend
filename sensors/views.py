from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view
from rest_framework.response import Response
from sensors.models import Sensor, SensorData
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
                sensorData = SensorData(
                    lpg=lpg, smoke=smoke, temperature=temperature)
                sensorData.save()
                return JsonResponse({'message': "Sensor Data Saved"}, status=201)
            except:
                return JsonResponse({'message': "Invalid Data"}, status=401)

    return JsonResponse({'message': "Invalid Data"}, status=401)

# get sensor data trend for the last 1 hour


def getValuesTrend(request):
    sensorData = SensorData.objects.all().order_by('-id')[0]
    value_id = sensorData.id
    if (value_id > 720):
        start = value_id - 720
        values = []
        # get data id in intervals of 120 (every 10mins)
        for i in range(start, start+721, 120):
            values.append(SensorData.objects.get(id=i))
            json_values = json.dumps(values)
        return JsonResponse({'values': json_values}, status=201)
    else:
        values = []
        for i in range(1, value_id+1, 120):  # get data id in intervals of 120 (every 10mins)
            values.append(SensorData.objects.get(id=i))
            # convert values to JSON and return it  as JSON_RESPONSE
            serializer = SensorDataSerializer(values, many=True)
            #json_values = json.dumps(values)
        return JsonResponse({'values': serializer.data}, status=201)
