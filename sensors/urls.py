from django.urls import path
from . import views

urlpatterns = [
    path('sensor_data/<str:pk>/', views.getSensorData),
    path('add_sensor_data/', views.postSensorData),
    path('sensor_data_list/<str:pk>/', views.getSensorDataList),
    path('sensor_data_trend/<str:pk>/', views.getValuesTrend),
    path('create_location/', views.createLocation),
    path('get_locations/', views.getLocations),
]
