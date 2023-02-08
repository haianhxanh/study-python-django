from datetime import date
from time import strftime

from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from rest_framework.response import Response
# from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from django.core.exceptions import PermissionDenied

from workspace.serializers import (
    AddUserProjectSerializer,
    CreateProjectSerializers,
    ListUserSerializer,
    ProjectDetailSerializer,
    ProjectSerializer,
    TaskSerializer,
    TimeRecordSerializer,
    TimeRecordStartSerializer,
    UpdateProjectSerializer,
    UserProjectSerializer,
    UserSerializer, ProjectTaskSerializer, ListProjectsSerializer, UserTaskSerializer,
    AddUserTaskSerializer, ProjectTimeRecordSerializer, TaskTimeRecordSerializer,
)
from .forms import RegistrationForm
from .models import Project, Task, TimeRecord, User, UserProject, UserTask
from .permissions import isProjectAdmin, IsProjectMember, IsGuest, isProjectAdminOrMember, isAuthenticated


# from workspace.permissions import isProjectAdmin


def home(request):
    return render(request, "workspace/home.html")


class RegistrationView(CreateView):
    template_name = "workspace/register.html"
    form_class = RegistrationForm

    # permission_classes = [isProjectAdmin]

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["next"] = self.request.GET.get("next")
        return context

    def get_success_url(self):
        next_url = self.request.POST.get("next")
        success_url = reverse("login")
        if next_url:
            success_url += "?next={}".format(next_url)

        return success_url


class ProfileView(UpdateView):
    model = User
    fields = ["name", "phone", "date_of_birth", "picture"]
    template_name = "workspace/profile.html"

    def get_success_url(self):
        return reverse("index")

    def get_object(self):
        return self.request.user


class Register(APIView):
    def post(self, request):
        form = UserCreationForm(request.POST)
        form.is_valid()
        form.save()
        username = form.cleaned_data.get("username")
        messages.success(request, f"Hi {username}, your account was successfully created")
        return redirect("home")


class TrackingStart(APIView):
    permission_classes = [IsAuthenticated]

    # kill all running
    def find_and_kill_all_running(self, user):
        running_timers = TimeRecord.objects.filter_running_timers(user)
        for timer in running_timers:
            timer.stop_time()

    # start new
    def post(self, request):
        serializer = TimeRecordStartSerializer(data=request.POST)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        start_time = strftime("%H:%M")
        date_now = date.today()
        self.find_and_kill_all_running(request.user)
        time_record = serializer.save(start_time=start_time, date=date_now, user=request.user)
        response_serializer = TimeRecordSerializer(time_record)
        # TimeRecord.objects.create(**serializer.validated_data, start_time=start_time, date=date_now,
        # user=request.user)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class StopAll(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        queryset = TimeRecord.objects.filter_running_timers(user=request.user)
        for tracker in queryset:
            tracker.stop_time()

        serializer = TimeRecordSerializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


# stop currently running one
class TrackingStop(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user: User = request.user
        try:
            current_timer = user.get_currently_running_timer()
        except TimeRecord.DoesNotExist:
            Response({}, status=status.HTTP_404_NOT_FOUND)

        current_timer.stop_time()
        serializer = TimeRecordSerializer(current_timer)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ListAllUsers(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ListUserSerializer

    def get_queryset(self, request):
        return User.objects.get(id=request.user.id)


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()


class ListUserProject(ListAPIView):
    pass


class UserProjectViewSet(ModelViewSet):

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            self.permission_classes = [IsProjectMember]
        else:
            self.permission_classes = [isProjectAdmin]
        return [isProjectAdminOrMember()]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return AddUserProjectSerializer
        return UserProjectSerializer

    def get_serializer_context(self):
        return {"project_id": self.kwargs["project_pk"]}

    def get_queryset(self):
        return UserProject.objects.filter(project_id=self.kwargs["project_pk"]).select_related("project")


class TimeRecordViewSet(ModelViewSet):
    serializer_class = TimeRecordSerializer
    permission_classes = [isProjectAdmin | IsProjectMember]

    def get_queryset(self):
        return TimeRecord.objects.filter(user=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        new_task = serializer.validated_data["task"]

        if new_task and not instance.user.user_tasks.filter(task=new_task).exists():
            raise ValidationError(f"User doesn't have task {new_task.id} assigned")

        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateTimeRecordViewSet(ModelViewSet):
    serializer_class = TimeRecordSerializer
    permission_classes = [isProjectAdmin | IsProjectMember]

    def get_queryset(self):
        return TimeRecord.objects.filter(user=self.request.user)


class TaskTimeRecordViewSet(ModelViewSet):
    serializer_class = TaskTimeRecordSerializer
    permission_classes = [isProjectAdmin | IsProjectMember]

    def get_queryset(self):
        return TimeRecord.objects.filter(task__project_id=self.kwargs["project_pk"])


class ProjectTimeRecordViewSet(ModelViewSet):
    serializer_class = TaskTimeRecordSerializer

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [isProjectAdminOrMember]
        else:
            permission_classes = [isProjectAdmin | IsProjectMember]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return TimeRecord.objects.filter(task__project_id=self.kwargs["project_pk"])


class ProjectViewSet(ModelViewSet):
    permission_classes = [isProjectAdmin | IsProjectMember]

    def get_serializer_class(self):
        if self.action == "list":
            return ProjectSerializer

        if self.request.method == "GET":
            return ProjectDetailSerializer

        if self.request.method == "PATCH":
            return UpdateProjectSerializer

        if self.request.method == "POST":
            return CreateProjectSerializers

        return ProjectSerializer

    def get_queryset(self):
        return Project.objects.filter(project_users__user_id=self.request.user.id, project_users__role__isnull=False)
        # .filter(Q(project_users__role__name="member") | Q(project_users__role__name="admin"))


class TaskViewSet(ModelViewSet):
    permission_classes = [isProjectAdminOrMember]

    def get_serializer_class(self):
        if self.request.method in ["POST", "PATCH"]:
            return ProjectTaskSerializer
        return TaskSerializer

    def get_serializer_context(self):
        return {"project_id": self.kwargs["project_pk"]}

    def get_queryset(self):
        return Task.objects.filter(project_id=self.kwargs["project_pk"]).select_related("project")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task = serializer.save()
        request.user.tasks.add(task)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class TaskUsers(ModelViewSet):
    permission_classes = [isProjectAdminOrMember]

    def get_serializer_class(self):
        if self.request.method in ["POST"]:
            return AddUserTaskSerializer
        return UserTaskSerializer

    def get_serializer_context(self):
        return {"task_id": self.kwargs["task_pk"]}

    def get_queryset(self):
        return UserTask.objects.filter(task__project_id=self.kwargs["project_pk"])
