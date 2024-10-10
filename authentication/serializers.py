from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from exceptions.CustomException import CustomException
from .models import User, Team, Task


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'phone_number', 'password', 'role')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        if 'username' in validated_data and User.objects.filter(username=validated_data['username']).exclude(
                id=instance.id).exists():
            raise CustomException('Username already exists.')
        return super().update(instance, validated_data)


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(max_length=100, required=True)


class TokenSerializer(serializers.Serializer):
    access_token = serializers.CharField()
    refresh_token = serializers.CharField()


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = ('id', 'name', 'created_at', 'updated_at')
        extra_kwargs = {
            'name': {'required': True}
        }


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'title', 'team', 'user', 'description', 'deadline', 'created_at')
        extra_kwargs = {
            'team': {'required': True}
        }


class TasksAddingSerializer(serializers.Serializer):
    task_id = serializers.IntegerField()
    users_id = serializers.ListField(child=serializers.IntegerField())


class TeamAddingSerializer(serializers.Serializer):
    team_id = serializers.IntegerField()
    users_id = serializers.IntegerField()
