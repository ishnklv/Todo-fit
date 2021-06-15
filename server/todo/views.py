from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filtersio
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Task, Label
from .permissions import IsOwnerOrReadOnly
from .serializers import TaskSerializer, LabelSerializer
from django import forms
from rest_framework import filters


class TaskFilter(filtersio.FilterSet):
    CHOICES = ((True, 'True'), (False, 'False'))

    is_completed = filtersio.BooleanFilter(field_name='completed', label="Completed",
                                           widget=forms.RadioSelect(
                                               attrs={'class': 'form-control', 'choices': CHOICES}))

    label = filtersio.CharFilter(field_name='label__title')

    class Meta:
        model = Task
        fields = ('is_completed', 'label')


class TaskViewSet(viewsets.ModelViewSet):
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    search_fields = ['title']
    queryset = Task.objects.filter(parent__isnull=True)
    filterset_class = TaskFilter
    serializer_class = TaskSerializer
    permission_classes = [IsOwnerOrReadOnly, ]
    authentication_classes = [JWTAuthentication, ]
    ordering_fields = ['title', 'date', 'completed', 'id']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(user=self.request.user)
        return Task.objects.none()


class LabelViewSet(viewsets.ModelViewSet):
    filter_backends = (DjangoFilterBackend, )
    filter_fields = ('title', )
    queryset = Label.objects.all()
    serializer_class = LabelSerializer
    permission_classes = [IsOwnerOrReadOnly, ]
    authentication_classes = [JWTAuthentication, ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return self.queryset.filter(user=self.request.user)