from django.db import models
from django.core.validators import MinValueValidator

class BodyPart(models.Model): 
    # 영상은 밑에 항목 중 적어도 1개 이상은 포함하고 있어야 함
    neck = models.BooleanField(default=False)
    wrist = models.BooleanField(default=False)
    eye = models.BooleanField(default=False)
    waist = models.BooleanField(default=False)
    field = models.BooleanField(default=False)

class Video(models.Model):
    title = models.CharField(max_length=50,null=True)
    length = models.IntegerField(validators=[MinValueValidator(0)],default=1,null=True) 
    youtubelink = models.CharField(max_length=100,null=True)
    thumbnail = models.ImageField(upload_to="thumbnails/", null=True)
    bodypart = models.ForeignKey(BodyPart,on_delete=models.CASCADE,related_name="video",null=True)