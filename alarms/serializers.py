from rest_framework import serializers
from alarms.models import AlarmContent
from alarms.models import Option
from users.serializers import UserSerializer

class AlarmContentSerializer(serializers.ModelSerializer):
    class Meta:
        model=AlarmContent
        fields='__all__'

class OptionSerializer(serializers.ModelSerializer):
    user_id = UserSerializer()
    class Meta:
        model=Option
        fields='__all__'
