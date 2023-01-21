from django.db.models import Q

from workspace.models import Project, User, Role, UserProject, Task
from rest_framework import permissions
from pprint import pprint


class isProjectAdmin(permissions.BasePermission):
    # def has_permission(self, request, view):
    #     role = Role.objects.get(name="admin")
    #     return request.user.role.name == role

    def _has_user(self, user, related_manager):
        return related_manager.filter(user=user).exists()

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Project):
            if self._has_user(request.user, obj.project_users):
                if obj.project_users.get(user=request.user).role.name == "admin":
                    return True
        elif isinstance(obj, Task):
            pass
        return False


class isProjectMember(permissions.BasePermission):
    pass
