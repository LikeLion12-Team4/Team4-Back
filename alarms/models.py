from django.db import models
from users.models import User
from videos.models import Video
# Create your models here.
class Option(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='options',null=True)
    interval = models.IntegerField(default=60,null=True) #알람간격 60분 디폴트 설정 -> 디폴트값 설정 정하기 
    is_alarm=models.BooleanField(null=False,default=True) #알람o 소리o 디폴트 설정 
    is_volumn=models.BooleanField(null=False,default=True)

class AlarmContent(models.Model):
    content=models.CharField(max_length=50,null=True)
    image=models.ImageField(upload_to='alarms/',max_length=None,null=True)

# class Alarm(models.Model):
#     user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='alarms',null=True)
#     video = models.ForeignKey(Video,on_delete=models.CASCADE,related_name='alarms',null=True)
#     content = models.ForeignKey(AlarmContent,on_delete=models.CASCADE,related_name='alarms',null=True)
#     option = models.ForeignKey(Option,on_delete=models.CASCADE,related_name='alarms',null=True)
    


