from django.db import models
from django.contrib.auth.models import AbstractUser
from videos.models import Video,BodyPart

class User(AbstractUser):
    recent_video = models.ForeignKey(Video, on_delete=models.SET_NULL,related_name='user_from_recent',null=True)
    bodypart = models.ManyToManyField(BodyPart,related_name='user')
    fullname = models.CharField(max_length=150,null=True)
    profile = models.ImageField(upload_to='users/',max_length=None,null=True)

class VideoLike(models.Model):
    video = models.ForeignKey(Video,on_delete=models.CASCADE,related_name="videolike_from_video",null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="videolike_from_user",null=True)

class Email(models.Model):
    verify_num = models.CharField(max_length=6,null=True)
    email = models.CharField(max_length=100, null = True)
    is_verified = models.BooleanField(null=False,default=False)
