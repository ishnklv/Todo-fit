from rest_framework import routers
from .views import TaskViewSet, TagViewSet, CommentViewSet
from fcm_django.api.rest_framework import FCMDeviceViewSet, FCMDeviceAuthorizedViewSet
from django.urls import path, include

router = routers.DefaultRouter()
router.register('tasks', TaskViewSet)
router.register('tags', TagViewSet)
router.register('comments', CommentViewSet)
router.register('devices', FCMDeviceViewSet)

urlpatterns = router.urls