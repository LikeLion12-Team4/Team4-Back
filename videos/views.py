from django.shortcuts import render

from users.models import User
from videos.models import BodyPart,Video
from videos.serializers import BodyPartSerializer, VideoSerializer
from users.serializers import UserSerializer
from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,
    ListCreateAPIView
)

from rest_framework.response import Response
from rest_framework import status

# video 썸네일은 pk가 있어야함 -> 이해 못했음
# user에 있는 recent_video 여기서 수정하기
# user가 누른 video만 보기

# ==========================================================================================
#                                       BodyPart View 
# ==========================================================================================

class BodyPartListAPIView(ListCreateAPIView): 
    queryset = BodyPart.objects.all()
    serializer_class = BodyPartSerializer
    lookup_field = 'id'
    #permission_class = [IsOwnerOrReadOnly]

class BodyPartRetrieveAPIView(RetrieveUpdateDestroyAPIView): 
    queryset = BodyPart.objects.all()
    serializer_class = BodyPartSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'bodypart_id'
    #permission_classes = [IsOwnerOrReadOnly]

# ==========================================================================================
#                                       Video View 
# ==========================================================================================

class VideoListAPIView(ListCreateAPIView): 
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'bodypart_id'
    #permission_classes = [IsOwnerOrReadOnly]

class VideoRetrieveAPIView(RetrieveUpdateDestroyAPIView): 
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'video_id'

    def retrieve(self, request, *args, **kwargs): # recent_video 최신화
        instance = self.get_object()
        request.user.recent_video = instance
        request.user.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    #permission_classes = [IsOwnerOrReadOnly]