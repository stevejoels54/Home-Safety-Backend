from django.urls import path
from . import views

urlpatterns = [
    path('sensorData/', views.getSensorData),
    path('add_sensorData/', views.postSensorData),
    path('sensorDataList/', views.getSensorDataList),
]
