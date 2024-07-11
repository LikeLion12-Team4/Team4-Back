from rest_framework import serializers
from alarms.models import AlarmContent
from alarms.models import Option
from users.serializers import UserSerializer

class AlarmContentSerializer(serializers.ModelSerializer):
    class Meta:
        model=AlarmContent
        fields='__all__'

class OptionSerializer(serializers.ModelSerializer):
    owner=UserSerializer(required=False)
    class Meta:
        model=Option
        fields= ['owner', 'interval', 'is_alarm', 'is_volume', 'fcm_token']
        extra_kwargs = {'fcm_token': {'required': False}, 'interval': {'required': False}, 
                        'is_alarm': {'required': False}, 'is_volume': {'required': False}}