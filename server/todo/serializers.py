from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Task, Label

User = get_user_model()


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'password')


class ChildTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('user', 'id', 'title', 'completed', 'image', 'date', 'parent')


class LabelSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.first_name', required=False)

    class Meta:
        model = Label
        fields = ('user', 'id', 'title')


class TaskSerializer(serializers.ModelSerializer):
    children = ChildTaskSerializer(many=True, required=False)
    user = serializers.ReadOnlyField(source='user.first_name', required=False)
    labels = serializers.ReadOnlyField(source='label.title', required=False)

    class Meta:
        model = Task
        fields = ('user', 'id', 'title', 'completed', 'image', 'date', 'children', 'parent', 'label', 'labels')