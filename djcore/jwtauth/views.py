from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from jwtauth.serializers import UserSerializer


def index(request):
    return render(request, 'jwtauth/index.html')

def user_content(request):
    return render(request, 'jwtauth/user.html')

def admin_panel(request):
    return render(request, 'jwtauth/admin.html')

class UserInfoAPIView(APIView):
    permission_classes = [IsAuthenticated,]
    def get(self, request):
        return Response({
            "username": request.user.username,
            "is_staff": request.user.is_staff
        })


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated,]
    def get(self, request):
        return Response({
            "username": request.user.username,
            "is_staff": request.user.is_staff
        })

class RoleSpecificContentView(APIView):
    pass

class CommonContentView(APIView):
    pass