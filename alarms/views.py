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
    
    def get_object(self):
        user = self.request.user
        option = Option.objects.get(owner=user)
        return option
    
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
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST )