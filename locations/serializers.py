from rest_framework import serializers
from locations.models import Hospital
from locations.models import Lesson


class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model=Hospital
        fields='__all__'
        #이미지 파일 별도 오버라이딩 필요 x => Meta에서 fields에서 해당 값 들어가기 때문

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model=Lesson
        
        fields='__all__'