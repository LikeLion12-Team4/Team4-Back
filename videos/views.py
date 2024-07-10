from django.shortcuts import render

from users.models import BodyPart,Video
from videos.serializers import VideoSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action,api_view
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
import cv2

# ==========================================================================================
#                                       Video View 
# ==========================================================================================

class VideoViewSet(viewsets.ModelViewSet): # url만 입력하면 영상 길이, 제목도 정해질 수 있게 해야되나 ?
    # 동영상 부위별로 나눠서 전달하도록
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'video_id'
    permission_classes = [IsAdminUser]

    def get_permissions(self):
        if self.action == "list":
            return [AllowAny()]
        elif self.action =="retrieve":
            return [IsAuthenticated()]
        return super().get_permissions()
    
    def extract_thumbnail_link(self,youtubelink): # 썸네일 추출 
        s = youtubelink.find("v=")+2
        e = youtubelink.find("&",s)
        if e == -1:
            e = len(youtubelink)
        thumbnail = youtubelink[s:e]
        return "https://img.youtube.com/vi/{}/default.jpg".format(thumbnail)

    # 동영상 생성, post는 관리자만 
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
        video = Video.objects.get(id = self.kwargs['video_id'])
        request.user.recent_video = video
        request.user.save()
        videoserializer = VideoSerializer(video)
        return Response(videoserializer.data,status=status.HTTP_200_OK)
    
@api_view(['GET'])
def open_webcam(request):
    # 웹캠 열기 (기본적으로 첫 번째 웹캠 사용)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        return
    while True:
        # 프레임 읽기
        ret, frame = cap.read()
        
        if not ret:
            break

        flipped_frame = cv2.flip(frame,1)
        # 프레임을 윈도우에 표시
        cv2.imshow('Webcam', flipped_frame)

        # ESC 키를 누르면 종료
        if cv2.waitKey(1) & 0xFF == 27:
            break

    # 웹캠 및 모든 윈도우 해제
    cap.release()
    cv2.destroyAllWindows()
    return Response(status=status.HTTP_200_OK)