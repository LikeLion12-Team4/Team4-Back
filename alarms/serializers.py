from rest_framework import serializers
from alarms.models import AlarmContent
from alarms.models import Option

class AlarmContentSerializer(serializers.ModelSerializer):
    class Meta:
        model=AlarmContent
        fields='__all__'

class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Option
        fields='__all__'
