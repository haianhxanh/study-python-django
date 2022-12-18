from djoser.serializers import (
    UserSerializer as BaseUserSerializer,
    UserCreateSerializer as BaseUserCreateSerializer,
)
from core.models import User


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            "id",
            "username",
            "password",
            "email",
            "first_name",
            "last_name",
        )


class UserSerializer(BaseUserSerializer):
    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
        )
