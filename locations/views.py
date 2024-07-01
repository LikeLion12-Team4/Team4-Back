from django.shortcuts import render
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
        lat_start = request.GET.get('lat_start',None)
        lat_end = request.GET.get('lat_end',None)
        long_start = request.GET.get('long_start',None)
        long_end = request.GET.get('long_end',None)
        #사용자 현재 위치만 주변 데이터들만 필터링하기 위해 Q()와 쿼리스트링 사용 
        q = Q()
        if lat_start and lat_end and long_start and long_end:
            q = Q(latitude__gte=lat_start) & Q(latitude__lte=lat_end)
            q &= Q(longitude__gte=long_start) & Q(longitude__lte=long_end)

        
        hospitals = Hospital.objects.filter(q)
        lessons = Lesson.objects.filter(q)

        hospitals_serializer = HospitalSerializer(hospitals, many=True)
        lessons_serializer = LessonSerializer(lessons, many=True)
        return Response({'lesson': lessons_serializer.data, 'hospital': hospitals_serializer.data}, status=status.HTTP_200_OK)