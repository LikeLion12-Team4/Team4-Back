from django.shortcuts import render
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect

from alarms.serializers import AlarmContentSerializer
from alarms.models import Option
from alarms.serializers import OptionSerializer
from users.models import User
from videos.models import Video
from videos.serializers import VideoSerializer
from alarms.models import AlarmContent

# Create your views here.
#알람 설정 여부 확인
#video title과 링크, username 필요 
#video도 랜덤 
#content-이미지세트는 랜덤 -> 총 세가지 => 따로 엔티티 만들어서 랜덤 돌리기

#알람 초기 설정 
class AlarmSetView(generics.CreateAPIView):
    serializer_class=OptionSerializer
    def perform_create(self, serializer):
        TEST_USER=User.objects.get(id=1)
        serializer.save(user=TEST_USER)
        # serializer.save(user=self.request.user)


#알림 설정 확인 및 수정
class OptionView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Option.objects.all()
    serializer_class=OptionSerializer
    lookup_field='id'
    lookup_url_kwarg='user_id'

    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except:
            #초기 설정 안 되어있을 때 이렇게 뜨는게 프론트한테 나을듯
            return Response({'알림 초기 설정':False},status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
  

#로그인이 되어있고, 알람 설정했으면 알람 확인 가능 
#알람 메세지 가져오기(만들기)
class AlarmView(generics.RetrieveAPIView):
    #비디오, content 다 그때마다 랜덤으로 가져오니까 알람모델 만들어서 인스턴스 생성할 필요 없을듯 
    #알람 모델, 시리얼라이저 다 일단 주석처리
    #근데 이렇게 하니까 상속을 전혀 활용하지 못하는 ........

    def get(self, request, *args, **kwargs): 
        #해당 유저
        user_id = kwargs.get('user_id')
        user = get_object_or_404(User, id=user_id)
        #로그인 구현되면 request.user.username으로 구현 예정 

        #비디오 랜덤 설정
        video=Video.objects.order_by("?").first()
        video_serializer=VideoSerializer(video) #비디오 title과 youtubelink가 필요 => 랜덤으로 가져오게 되면서 이걸 맞게 가져오게할 시리얼라이저가 없음 ..
        #content 랜덤설정 
        content=AlarmContent.objects.order_by("?").first()
        content_serializer=AlarmContentSerializer(content)
        
        #title과 link만 가져오기
        video_data = {
            'title': video_serializer.data.get('title'),
            'youtubelink': video_serializer.data.get('youtubelink')
        }

        data={
            'username':user.username,
            'content':content_serializer.data,
            'video':video_data,
        } 
        return Response(data,status=status.HTTP_200_OK)



    



