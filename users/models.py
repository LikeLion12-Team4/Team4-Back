from django.db import models
from django.contrib.auth.models import AbstractUser
from videos.models import Video

class PainPart(models.Model):
    painname = models.CharField(max_length=10,null=True)
    
class User(AbstractUser):
    recent_video = models.ForeignKey(Video, on_delete=models.CASCADE,related_name='user_from_recent',null=True)
    painpart = models.ForeignKey(PainPart,on_delete=models.CASCADE,related_name="user_from_painpart",null=True,blank=False)

class VideoLike(models.Model):
    video = models.ForeignKey(Video,on_delete=models.CASCADE,related_name="videolike_from_video",null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="videolike_from_user",null=True)