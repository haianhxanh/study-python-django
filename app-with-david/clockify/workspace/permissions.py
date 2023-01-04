from workspace.models import Project, User, Role
from rest_framework import permissions


class isProjectAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        role = Role.objects.get(name="admin")

        return request.user.role == role

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Project):
            # wont work
            if request.user in obj.project_users:
                if obj.project_users.get(user=request.user).role.name == "member" and permissions.SAFE_METHODS:
                    return True
        return False
