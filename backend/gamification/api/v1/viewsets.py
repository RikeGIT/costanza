from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from gamification.models import Badge, UserBadge
from .serializers import BadgeSerializer, UserBadgeSerializer

class BadgeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'])
    def mine(self, request):
        """Retorna apenas as medalhas do usuário logado"""
        user_badges = UserBadge.objects.filter(user=request.user)
        serializer = UserBadgeSerializer(user_badges, many=True)
        return Response(serializer.data)