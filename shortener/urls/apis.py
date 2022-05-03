from django.http import Http404
from rest_framework import viewsets, permissions, status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.decorators import renderer_classes, action

from shortener.models import ShortenedUrls
from shortener.urls.serializers import UrlListSerializer, UrlCreateSerializer
from shortener.utils import MsgOK, url_count_changer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = ShortenedUrls.objects.all().order_by("-created_at") #
    serializer_class = UrlListSerializer
    permission_classes = [permissions.IsAuthenticated] # 로그인된 유저만 사용


    def create(self, request, *args, **kwargs):
        serializer = UrlCreateSerializer(data=request.data)
        if serializer.is_valid():
            rtn = serializer.create(request, serializer.data)
            return Response(UrlListSerializer(rtn).data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        # Detail Get
        queryset = self.get_queryset().filter(pk=kwargs['pk']).first()
        serializer = UrlListSerializer(queryset)
        return Response(serializer.data)

    def update(self, request):
        pass

    def partial_update(self, request):
        pass

    @renderer_classes([JSONRenderer])
    def destroy(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(pk=kwargs['pk'], creator_id=request.user.id)
        if not queryset.exists():
            raise Http404
        queryset.delete()
        url_count_changer(request, False)
        return MsgOK()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().all()
        serializer = UrlListSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def add_click(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(pk=kwargs['pk'], creator_id=request.user.id)
        if not queryset.exists():
            raise Http404
        rtn = queryset.first().clicked()
        serializer = UrlListSerializer(rtn)
        return Response(serializer.data)
