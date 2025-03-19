from rest_framework.permissions import BasePermission
from .utils import is_blacklisted, is_whitelisted


class IsTokenValid(BasePermission):
    def has_permission(self, request, view):
        auth_header = request.headers.get('Authorization')

        if not auth_header or not auth_header.startswith('Bearer '):
            return False

        access_token = auth_header.split(' ')[1]

        if is_blacklisted(access_token):
            return False

        return True
