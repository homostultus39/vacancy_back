"""
URL configuration for djcore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from jwtauth import views
from jwtauth.views import UserInfoAPIView, LogoutAPIView, CommonContentView, RoleSpecificContentView

urlpatterns = [
    path('', views.index, name='home'),
    path('user-content/', views.user_content, name="user_content"),
    path('admin-content/', views.admin_content, name="admin_content"),
    path('api/me/', UserInfoAPIView.as_view(), name="user_info"),
    path('api/common-content/', CommonContentView.as_view(), name="common_content"),
    path('api/role-content/', RoleSpecificContentView.as_view(), name="role_content"),
    path('api/logout/', LogoutAPIView.as_view(), name="logout_api"),
]
