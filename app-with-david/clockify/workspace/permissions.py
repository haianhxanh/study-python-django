from django.db.models import Q
from django.http import Http404
from rest_framework.permissions import SAFE_METHODS

from workspace.models import Project, User, Role, UserProject, Task, TimeRecord, UserTask
from rest_framework import permissions
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from pprint import pprint


class isAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated


class isProjectAdminOrMember(permissions.BasePermission):

    def has_permission(self, request, view):
        project_pk = view.kwargs.get('project_pk', None)
        try:
            user_role = UserProject.objects.get(project_id=project_pk, user_id=request.user.id).role.name
        except UserProject.DoesNotExist:
            return False
        if user_role == 'admin':
            return request.method in ["GET", "POST", "DELETE", "PUT", "PATCH"]
        if user_role == 'member':
            return request.method in ["GET"]
        return False


class isProjectAdmin(permissions.BasePermission):

    def _has_user(self, user, related_manager):
        return related_manager.filter(user=user).exists()

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Project):
            if self._has_user(request.user, obj.project_users):
                if obj.project_users.get(user=request.user).role.name == "admin":
                    return True
        elif isinstance(obj, UserProject):
            admin = UserProject.objects.get(project_id=obj.project.id, role__name="admin").user
            if admin == request.user:
                return True
        elif isinstance(obj, TimeRecord):
            # if the time record is not assigned to any task and belongs to user, allow him to edit
            if obj.task is not None:
                if self._has_user(request.user, obj.task.project.project_users):
                    if obj.task.project.project_users.get(user=request.user).role.name == "admin":
                        return True
            else:
                return True
        elif isinstance(obj, UserTask):
            if self._has_user(request.user, obj.task.project.project_users):
                return True
        else:
            return False


class IsProjectMember(permissions.BasePermission):

    def _has_user(self, user, related_manager):
        return related_manager.filter(user=user).exists()

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Project):
            if self._has_user(request.user, obj.project_users):
                if obj.project_users.get(user=request.user).role.name == "member":
                    if request.method in permissions.SAFE_METHODS:
                        return True
        elif isinstance(obj, TimeRecord):
            # if the time record is not assigned to any task and belongs to user, allow him to edit
            if obj.task is not None:
                if self._has_user(request.user, obj.task.project.project_users):
                    if obj.task.project.project_users.get(user=request.user).role.name == "member":
                        if obj.user == request.user:
                            return True
                        else:
                            if request.method in permissions.SAFE_METHODS:
                                return True
                    return False
            else:
                return True

        else:
            return False


# temporary test
class IsGuest(permissions.BasePermission):
    """this class is about ..."""
    def _has_user(self, user, related_manager):
        """this method is about"""
        return related_manager.filter(user=user).exists()

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, Project):
            if self._has_user(request.user, obj.project_users):
                if obj.project_users.get(user=request.user).role.name == "":
                    if request.method in permissions.SAFE_METHODS:
                        return True
        else:
            return False
