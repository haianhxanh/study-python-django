from django.urls import include, path
from . import views
from rest_framework import permissions


project_list = views.ProjectViewSet.as_view({'get': 'list', 'post': 'create'})

project_details = views.ProjectViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

project_users_list = views.UserProjectViewSet.as_view({'get': 'list', 'post': 'create'})

project_user_details = views.UserProjectViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

project_tasks_list = views.TaskViewSet.as_view({'get': 'list', 'post': 'create'})

project_task_details = views.TaskViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

time_records_list = views.TimeRecordViewSet.as_view({'get': 'list'})

urlpatterns = [
    path("", views.home, name="home"),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    path("register/", views.Register.as_view(), name="register"),
    path("projects/", project_list, name="list-projects"),
    path("projects/<int:pk>/", project_details, name="project-details"),
    path("projects/<int:project_pk>/users/", project_users_list, name="list-project-users"),
    path("projects/<int:project_pk>/users/<pk>/", project_user_details, name="project-user-detail"),
    path("projects/<int:project_pk>/tasks/", project_tasks_list, name="list-project-tasks"),
    path("projects/<int:project_pk>/tasks/<pk>/", project_task_details, name="project-task-details"),
    path("users/", views.ListAllUsers.as_view(), name="list-users"),
    path("tracking", time_records_list, name="list-time-records"),
    path("tracking/start", views.TrackingStart.as_view(), name="tracker-start"),
    path("tracking/stop", views.TrackingStop.as_view(), name="tracker-stop"),
    path('__debug__/', include('debug_toolbar.urls')),
]

