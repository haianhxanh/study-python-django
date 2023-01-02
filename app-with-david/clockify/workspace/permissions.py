from workspace.models import Permission, User
from rest_framework import permissions


class isProjectAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.User)
