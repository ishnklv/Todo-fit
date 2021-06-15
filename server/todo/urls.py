from rest_framework import routers
from .views import TaskViewSet, LabelViewSet
from django.urls import path, include

router = routers.DefaultRouter()
router.register('tasks', TaskViewSet)
router.register('labels', LabelViewSet)

urlpatterns = router.urls