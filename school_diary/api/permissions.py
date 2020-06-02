from rest_framework import permissions
from api import models


class APIUserPermission(permissions.BasePermission):
    """
    Check if user is allowed to view API. Using API
    is allowed only if user exists in AllowedToUseAPIList
    or user is superuser (root with account_type = 0).
    """
    def has_permission(self, request, view):
        return request.user.is_superuser or \
            models.AllowedToUseAPIList.objects.filter(user=request.user).exists()
