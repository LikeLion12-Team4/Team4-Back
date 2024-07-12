from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework import views
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated,IsAdminUser

from alarms.serializers import AlarmContentSerializer
from alarms.models import Option
from alarms.serializers import OptionSerializer

class OptionView(generics.RetrieveUpdateAPIView):
    queryset=Option.objects.all()
    permission_classes=[IsAuthenticated]
    serializer_class=OptionSerializer
    
    def get_object(self,request):
        user = request.user
        option = Option.objects.get(owner=user)
        return option

    def put(self, request, *args, **kwargs):
        return self.patch(self, request, *args, **kwargs)    

    # def put(self, request, *args, **kwargs):
    #     return self.patch
        # interval = request.data.get('interval')
        # is_alarm = request.data.get('is_alarm')
        # try:
        #     option = Option.objects.get(interval = interval, is_alarm = is_alarm)
        # except Option.DoesNotExist:
        #     return Response({"error":"옵션이"})

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