from rest_framework import permissions
from apps.api import models


class APIUserPermission(permissions.BasePermission):
    """
    Check if user is allowed to view API. Using API
    is allowed only if user exists in AllowedToUseAPIList
    or user is superuser (root with account_type = 0).
    """
    message = "You must be in whitelist or be logged" + \
        "in as root administrator to use the API."

    def has_permission(self, request, view):
        return request.user.is_authenticated and (
                request.user.is_superuser or
                models.AllowedToUseAPIList.objects.filter(user=request.user).exists())


class InBuiltAPIPermission(permissions.BasePermission):
    message = "Request to in-built API must be called with Ajax"

    def has_permission(self, request, view):
        return request.is_ajax()
