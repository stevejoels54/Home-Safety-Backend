from django.urls import path
from . import views

urlpatterns = [
    path('sensor_data/', views.getSensorData),
    path('add_sensor_data/', views.postSensorData),
    path('sensor_data_list/', views.getSensorDataList),
    path('sensor_data_trend/', views.getValuesTrend),
]
