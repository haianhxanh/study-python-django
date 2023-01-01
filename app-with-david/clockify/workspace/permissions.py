from workspace.models import Permission

from rest_framework.permissions import BasePermission


class isProjectAdmin(BasePermission):
    def has_permission(self, request, view):
        return super().has_permission(request, view)
