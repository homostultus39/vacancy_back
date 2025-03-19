import time

import jwt
from django.conf import settings
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from jwtauth.permissions import IsTokenValid
from jwtauth.utils import blacklist_token

def index(request):
    return render(request, 'jwtauth/index.html')

def user_content(request):
    return render(request, 'jwtauth/user.html')

def admin_content(request):
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
    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            auth_data = request.headers['Authorization']
            access_token = auth_data.split(' ')[1]
            decoded_token = jwt.decode(access_token, settings.SECRET_KEY, algorithms=['HS256'])

            expires_in = decoded_token['exp'] - int(time.time())

            blacklist_token(access_token, expires_in)

            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Successfully logged out."})
        except Exception as e:
            return Response({"message": str(e)})

class CommonContentView(APIView):
    permission_classes = [IsAuthenticated, IsTokenValid]
    def get(self, request):
        return Response({"data": "Общий контент для всех авторизованных пользователей"})

class RoleSpecificContentView(APIView):
    permission_classes = [IsAuthenticated, IsTokenValid]
    def get(self, request):
        if request.user.is_staff:
            return Response({"data": "Контент, доступный только админам"})
        else:
            return Response({"data": "Контент, доступный только пользователям"})
