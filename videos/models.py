from django.db import models
from django.core.validators import MinValueValidator

class BodyPart(models.Model):     
    partname = models.CharField(max_length=10,null=True)
    
class Video(models.Model):
    title = models.CharField(max_length=50,null=True)
    length = models.IntegerField(validators=[MinValueValidator(0)],default=1,null=True) 
    youtubelink = models.CharField(max_length=100,null=True)
    thumbnail = models.ImageField(upload_to="thumbnails/", null=True)
    bodypart = models.ForeignKey(BodyPart,on_delete=models.CASCADE,related_name="video",null=True)