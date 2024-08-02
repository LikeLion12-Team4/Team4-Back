from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework import views
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated,IsAdminUser

from alarms.serializers import AlarmContentSerializer
from alarms.models import Option,AlarmContent
from alarms.serializers import OptionSerializer
from videos.models import BodyPart
from django.shortcuts import render

class OptionView(generics.RetrieveUpdateAPIView):
    queryset=Option.objects.all()
    permission_classes=[IsAuthenticated]
    serializer_class=OptionSerializer
    
    def get_object(self):
        user = self.request.user
        option = Option.objects.get(owner=user)
        return option
    
    # fcm token을 갱신 해야함
    def update(self, request):
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


#content 생성 뷰(이미지 업로드)
#관리자만
class AlarmContentView(views.APIView):
    permission_classes=[IsAdminUser]
    parser_classes = (MultiPartParser, FormParser)
    serializer_class = AlarmContentSerializer

    def post(self, request, *args, **kwargs):
        bodyname = request.data.get('bodypart') 
        content = request.data.get('content')
        image = request.data.get('image')
        try:
            for bp in BodyPart.objects.all(): # bodypart 객체에 user 추가
                if bp.bodyname == bodyname:
                    bodypart = bp
                    break
        except BodyPart.DoesNotExist:
            return Response({"error":"부위가 존재하지 않습니다."},status=status.HTTP_404_NOT_FOUND)
        
        alarmcontent = AlarmContent.objects.create(bodypart=bodypart,content=content,image=image)
        alarmcontent.save()
        serializer = self.serializer_class(alarmcontent)
        return Response(serializer.data,status=status.HTTP_201_CREATED)