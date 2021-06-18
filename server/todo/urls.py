from rest_framework import routers
from .views import TaskViewSet, LabelViewSet, CommentViewSet
from fcm_django.api.rest_framework import FCMDeviceViewSet, FCMDeviceAuthorizedViewSet
from django.urls import path, include

router = routers.DefaultRouter()
router.register('tasks', TaskViewSet)
router.register('labels', LabelViewSet)
router.register('comments', CommentViewSet)
router.register('devices', FCMDeviceViewSet)

urlpatterns = router.urls