from rest_framework import serializers
from workspace.models import User, TimeRecord


class ListUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class ListTimeRecordsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeRecord
        fields = "__all__"


class TimeRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimeRecord
        fields = "__all__"


class TimeRecordStartSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TimeRecord
        fields = ["description"]
        