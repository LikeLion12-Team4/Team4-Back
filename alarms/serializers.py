from rest_framework import serializers
from alarms.models import AlarmContent
from alarms.models import Option
# from alarms.models import Alarm

class AlarmContentSerializer(serializers.ModelSerializer):
    class Meta:
        model=AlarmContent
        fields='__all__'

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Option
        fields='__all__'
    
# class AlarmSerializer(serializers.ModelSerializer):
#     # user=UserSerializer()
#     # video=VideoSerializer()
#     option=OptionSerializer()
#     content=AlarmContentSerializer

#     user=serializers.SlugRelatedField(
#         many=False,
#         read_only=True,
#         slug_field='username'
#     )
#     video=serializers.SlugRelatedField(
#         many=False,
#         read_only=True,
#         slug_field='youtubelink'
#     ) #video링크만 시리얼라이저
#     class Meta:
#         model=Alarm
#         fields='__all__'
