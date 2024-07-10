from rest_framework import generics
from locations.models import Hospital
from locations.serializers import HospitalSerializer
from locations.models import Lesson
from locations.serializers import LessonSerializer
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Q

# Create your views here.

#권한 있어야만 지도 볼 수 있는지? 비회원도 지도는 볼 수 있게끔 하면 좋을듯 
class LocationListView(generics.ListAPIView):
    def get(self, request, *args, **kwargs):
        lat = request.GET.get('lat',None)
        long = request.GET.get('long',None)
        #사용자 현재 위치만 주변 데이터들만 필터링하기 위해 Q()와 쿼리스트링 사용 
        q = Q()
        if lat and long:
            q = Q(latitude__gte=lat-100) & Q(latitude__lte=lat+100)
            q &= Q(longitude__gte=long-30) & Q(longitude__lte=long+30)

        hospitals = Hospital.objects.filter(q)
        lessons = Lesson.objects.filter(q)

        hospitals_serializer = HospitalSerializer(hospitals, many=True)
        lessons_serializer = LessonSerializer(lessons, many=True)
        return Response({'lesson': lessons_serializer.data, 'hospital': hospitals_serializer.data}, status=status.HTTP_200_OK)