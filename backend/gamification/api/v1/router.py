from rest_framework.routers import DefaultRouter
from .viewsets import BadgeViewSet

router = DefaultRouter()
router.register(r'badges', BadgeViewSet, basename='badge')