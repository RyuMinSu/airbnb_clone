from rest_framework.serializers import ModelSerializer
from .models import User


class TinyUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("avatar", "name", "username")


class PrivateUserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ("password", "id", "is_staff", "is_active", "is_superuser", "first_name", "last_name", "groups", "user_permissions",)