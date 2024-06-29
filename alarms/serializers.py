from rest_framework import serializers
from alarms.models import Alarm
from users.serializers import UserSerializer
from videos.serializers import VideoSerializer

class AlarmSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    video=serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='youtubelink'
    ) #video링크만 시리얼라이저

    class Meta:
        model=Alarm
        fields='__all__'