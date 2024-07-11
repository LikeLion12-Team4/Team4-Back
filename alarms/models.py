from django.db import models
from users.models import User, BodyPart
from django.utils import timezone

# fcm_token 필드 추가
# 지난 번에 알람 받은 시간 필드 추가
class Option(models.Model):
    owner = models.OneToOneField(User,on_delete=models.CASCADE,related_name='options',null=True)
    interval = models.IntegerField(default=10,null=False) #알람간격 60분 디폴트 설정 -> 디폴트값 설정 정하기 
    is_alarm=models.BooleanField(null=False,default=False) #알람o 소리o 디폴트 설정 
    is_volumn=models.BooleanField(null=False,default=False)
    last_push_time=models.DateTimeField(null=False, default=timezone.now())
    fcm_token=models.CharField(null=True, max_length=200)

class AlarmContent(models.Model):
    content=models.CharField(max_length=50,null=True)
    image=models.ImageField(upload_to='alarms/',max_length=None,null=True)
    bodypart = models.ForeignKey(BodyPart, on_delete=models.CASCADE, related_name='alarm_content', null=True)

    def __str__(self):
        return self.content