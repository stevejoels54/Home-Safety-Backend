from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view
from rest_framework.response import Response
from customuser.models import CustomUser
from customuser.serializers import UserSerializer
import json


def users_list(request):
    users = CustomUser.objects.all()
    serializer = UserSerializer(users, many=True)

    return JsonResponse({'users': serializer.data})


@require_http_methods(["POST"])
def loginUser(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except:
            data = {}
        if data:
            try:
                email = data['email']
                password = data['password']
                user = authenticate(request, email=email, password=password)
            except:
                user = None
            if user is not None:
                login(request, user)
                return JsonResponse({'message': "Login Successful"}, status=201)

    return JsonResponse({'message': "Invalid Email or Password"}, status=401)

# Create your views here.
