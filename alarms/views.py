from django.shortcuts import render
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework import views
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework import exceptions
from rest_framework.permissions import IsAuthenticated,IsAdminUser


from alarms.serializers import AlarmContentSerializer
from alarms.models import Option
from alarms.serializers import OptionSerializer
from videos.models import Video
from videos.serializers import VideoSerializer
from alarms.models import AlarmContent
from alarms.permissions import IsOwner

# Create your views here.
#알람 초기 설정 (추가)
#로그인 유저만
class AlarmSetView(generics.CreateAPIView):
    permission_classes=[IsAuthenticated]
    serializer_class=OptionSerializer
    def perform_create(self, serializer):
        if Option.objects.filter(user_id=self.request.user).exists(): #option은 일대일관계로 이미 존재하면 생성할 때 오류남
            raise exceptions.ValidationError({'error': '이미 존재'}) #그래서 400에러 발생하도록
        serializer.save(user_id=self.request.user,is_option=True) #생성될때 True값으로 바뀌도록 하여서 설정 여부 확인할 수 있게

        

#알림 설정 확인 및 수정 (변경)
#로그인0,해당 유저만
class OptionView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=[IsOwner]
    #url 파라미터 사용 안 하는 방향으로 변경 => 자기 알림만 확인 0 =? 그럼 permission 필요 없어지나?? 근데 애초에 로그인해야 알림 설정할 수 있는 화면 나타나긴 함
    serializer_class = OptionSerializer
    def get_object(self):
        try:
            return Option.objects.get(user=self.request.user)
        except Option.DoesNotExist:
            raise exceptions.NotFound({'error':'알람 설정 존재x'}) #404에러
    #is_option필드로 알람 설정여부 확인 가능 

        

#로그인이 되어있고, 알람 설정했으면 알람 확인 가능 =>로그인 여부 : permission 사용, 알람 설정 여부 : 프론트에서 확인 ?
#알람 메세지 가져오기(만들기)
class MessageView(generics.RetrieveAPIView):
    permission_classes=[IsAuthenticated]
    def get(self, request, *args, **kwargs): 
        #비디오 랜덤 설정
        video=Video.objects.order_by("?").first()
        video_serializer=VideoSerializer(video)
        #content 랜덤설정 
        content=AlarmContent.objects.order_by("?").first()
        content_serializer=AlarmContentSerializer(content)
        #title과 link만 가져오기
        video_data = {
            'title': video_serializer.data.get('title'),
            'youtubelink': video_serializer.data.get('youtubelink')
        }
        data={
            'username':request.user.username,
            'content':content_serializer.data,
            'video':video_data,
        } 
        return Response(data,status=status.HTTP_200_OK)

#content 생성 뷰(이미지 업로드)
#관리자만
class AlarmContentView(views.APIView):
    permission_classes=[IsAdminUser]
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = AlarmContentSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST )
    



