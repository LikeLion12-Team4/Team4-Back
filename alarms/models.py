from django.db import models
from users.models import User
from videos.models import Video
# Create your models here.
class Alarm(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='alarms',null=True)
    video = models.ForeignKey(Video,on_delete=models.CASCADE,related_name='alarms',null=True)
    content=models.CharField(max_length=50,null=True)
    interval = models.IntegerField(default=60,null=True) #알람간격 디폴트값 설정 필요
    image=models.ImageField(upload_to='alarms/', height_field=200, width_field=200, max_length=None,null=True)
    is_alarm=models.BooleanField(null=False,default=True) #디폴트값 설정 
    is_volumn=models.BooleanField(null=False,default=True)