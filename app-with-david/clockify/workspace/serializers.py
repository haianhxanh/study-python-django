from asyncore import read
from pkg_resources import require
from rest_framework import serializers
from workspace.models import Currency, Project, Task, User, TimeRecord, UserProject, UserTask


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ["shortcut_name"]


class ListUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name"]


class TaskSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "name"]


class UserTaskSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = UserTask
        fields = ["username"]


class TaskSerializer(serializers.ModelSerializer):
    task_users = UserTaskSerializer(many=True)

    class Meta:
        model = Task
        fields = ["id", "name", "max_allocated_hours", "task_users"]


class TaskItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"


class TaskProjectSimpleSerializer(serializers.ModelSerializer):
    task_project = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ["id", "name", "task_project"]

    def get_task_project(self, Task):
        return Task.project.name


class TimeRecordSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    task = TaskProjectSimpleSerializer()

    class Meta:
        model = TimeRecord
        fields = ["id", "description", "start_time", "end_time", "date", "task", "user"]

    def get_user(self, TimeRecord):
        return TimeRecord.user.username

    def get_task(self, TimeRecord):
        return TimeRecord.task.name


class TimeRecordStartSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeRecord
        fields = ["description", "task"]


class TimeRecordStopSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeRecord
        fields = ["description", "task", "start_time", "end_time"]


class UserProjectSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source="user.username")
    role = serializers.ReadOnlyField(source="role.name")
    user_id = serializers.ReadOnlyField(source="user.id")

    class Meta:
        model = UserProject
        fields = ["username", "user_id", "role"]


class AddUserProjectSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    role_id = serializers.IntegerField()

    def save(self, **kwargs):
        project_id = self.context["project_id"]
        user_id = self.validated_data["user_id"]
        role_id = self.validated_data["role_id"]

        try:
            user_project = UserProject.objects.get(project_id=project_id, user_id=user_id, role_id=role_id)
            user_project.save()
        except UserProject.DoesNotExist:
            self.instance = UserProject.objects.create(project_id=project_id, **self.validated_data)

        return self.instance

    class Meta:
        model = UserProject
        fields = ["user_id", "project_id", "role_id"]


class TaskSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "name"]


class ProjectSerializer(serializers.ModelSerializer):
    project_users = UserProjectSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ["id", "name", "project_users"]

    def get_project_users(self, Project):
        return Project.user.username


class UpdateProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"


class CreateProjectSerializers(serializers.ModelSerializer):
    def create(self, validated_data):
        return Project.objects.create(**validated_data)

    class Meta:
        model = Project
        fields = ["id", "name", "description", "hourly_rate", "currency"]


class ProjectDetailSerializer(serializers.ModelSerializer):
    tasks = TaskSimpleSerializer(many=True)
    project_users = UserProjectSerializer(many=True)
    currency = CurrencySerializer()

    class Meta:
        model = Project
        fields = ["id", "name", "description", "hourly_rate", "currency", "tasks", "project_users"]

    def get_currency(self, Project):
        return Project.currency.shortcut_name
