from django.shortcuts import render

from videos.models import BodyPart,Video
from videos.serializers import BodyPartSerializer, VideoSerializer
from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,
    ListCreateAPIView
)

from rest_framework.response import Response
from rest_framework import status

# video 썸네일은 pk가 있어야함 -> 이해 못했음

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
    
    def perform_create(self, serializer):
        try: 
            video = Video.objects.get(id = self.kwargs['video_id'])
        except Video.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer.save()

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