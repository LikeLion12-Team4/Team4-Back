from django.shortcuts import render

from users.models import BodyPart,Video
from videos.serializers import VideoSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

# ==========================================================================================
#                                       Video View 
# ==========================================================================================

class VideoViewSet(viewsets.ModelViewSet): # url만 입력하면 영상 길이, 제목도 정해질 수 있게 해야되나 ?
    # 동영상 부위별로 나눠서 전달하도록
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'video_id'
    #permission_classes = [IsOwnerOrReadOnly]
    
    def extract_thumbnail_link(self,youtubelink): # 썸네일 추출 
        s = youtubelink.find("v=")+2
        e = youtubelink.find("&",s)
        if e == -1:
            e = len(youtubelink)
        thumbnail = youtubelink[s:e]
        return "https://img.youtube.com/vi/{}/default.jpg".format(thumbnail)

    # 동영상 생성
    def create(self, request, *args, **kwargs):
        title = request.data.get('title')
        length = request.data.get('length')
        youtubelink = request.data.get('youtubelink')
        bodyname = request.data.get('bodypart')
        thumbnail= self.extract_thumbnail_link(youtubelink)

        bodypart = BodyPart.objects.get(bodyname=bodyname)
        video = Video.objects.create(title=title,
                                     length = length,
                                     youtubelink=youtubelink,
                                     thumbnail = thumbnail,
                                     bodypart = bodypart)
        video.save()
        serializer = self.get_serializer(video)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    # 동영상 리스트 조회
    def list(self, request, *args, **kwargs):
        dict = {}
        for bodypart in BodyPart.objects.all():
            video = Video.objects.filter(bodypart=bodypart)
            videoserializer = VideoSerializer(video,many=True)
            dict[bodypart.bodyname]=videoserializer.data
        return Response(dict,status=status.HTTP_200_OK)
    
    # 특정 동영상 보기 -> recent_video 업데이트
    def retrieve(self, request, *args, **kwargs):
        if request.user.is_authenticated: 
            video = Video.objects.get(id = self.kwargs['video_id'])
            request.user.recent_video = video
            request.user.save()
            videoserializer = VideoSerializer(video)
            return Response(videoserializer.data,status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
        #permission_classes = [IsOwnerOrReadOnly]