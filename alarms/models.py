from django.db import models
from users.models import User
from videos.models import Video
# Create your models here.
class Option(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='options',null=True)
    is_option=models.BooleanField(null=False,default=False) #초기 설정 여부 확인 필드 추가, 디폴트 = False
    interval = models.IntegerField(default=60,null=True) #알람간격 60분 디폴트 설정 -> 디폴트값 설정 정하기 
    is_alarm=models.BooleanField(null=False,default=True) #알람o 소리o 디폴트 설정 
    is_volumn=models.BooleanField(null=False,default=True)

class AlarmContent(models.Model):
    content=models.CharField(max_length=50,null=True)
    image=models.ImageField(upload_to='alarms/',max_length=None,null=True)

    def __str__(self):
        return self.content


