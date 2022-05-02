from rest_framework import viewsets, permissions

from shortener.models import ShortenedUrls
from shortener.urls.serializers import UrlListSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = ShortenedUrls.objects.all().order_by("-created_at") #
    serializer_class = UrlListSerializer
    permission_classes = [permissions.IsAuthenticated] # 로그인된 유저만 사용
