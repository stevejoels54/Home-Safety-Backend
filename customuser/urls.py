from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginUser),
    path('users/', views.users_list),
]
