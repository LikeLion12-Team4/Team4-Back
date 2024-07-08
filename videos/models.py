from django.db import models
from django.core.validators import MinValueValidator

class BodyPart(models.Model):
    bodyname = models.CharField(max_length=10,null=True)

class Video(models.Model):
    title = models.CharField(max_length=50,null=True)
    length = models.IntegerField(validators=[MinValueValidator(0)],default=1,null=True) 
    youtubelink = models.CharField(max_length=100,null=True)
    thumbnail = models.CharField(max_length=100,null=True)
    bodypart = models.ForeignKey(BodyPart,on_delete=models.SET_NULL,related_name="video",null=True)

