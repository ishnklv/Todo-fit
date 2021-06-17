from rest_framework import routers
from .views import TaskViewSet, LabelViewSet, CommentViewSet
from django.urls import path, include

router = routers.DefaultRouter()
router.register('tasks', TaskViewSet)
router.register('labels', LabelViewSet)
router.register('comments', CommentViewSet)

urlpatterns = router.urls