from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Task, Label, Comment

User = get_user_model()


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'password')


class ChildTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('user', 'id', 'title', 'completed', 'image', 'date', 'parent', 'is_notific', 'remind')


class TagSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.first_name', required=False)

    class Meta:
        model = Label
        fields = ('user', 'id', 'title')


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.first_name', required=False)

    class Meta:
        model = Comment
        fields = ('id', 'user', 'title', 'date')


class TaskSerializer(serializers.ModelSerializer):
    children = ChildTaskSerializer(many=True, required=False)
    user = serializers.ReadOnlyField(source='user.first_name', required=False)
    tags = TagSerializer(many=True, required=False)
    comments = CommentSerializer(many=True, required=False)

    class Meta:
        model = Task
        fields = ('user', 'id', 'title', 'completed', 'image', 'date', 'children', 'parent', 'is_notific', 'remind', 'comments', 'labels',)