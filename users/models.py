from django.db import models
from django.contrib.auth.models import AbstractUser
from videos.models import Video

class PainPart(models.Model):
    # 사용자는 밑에 항목 중 적어도 1개 이상은 선택해야 함
    neck = models.BooleanField(default=False)
    wrist = models.BooleanField(default=False)
    eye = models.BooleanField(default=False)
    waist = models.BooleanField(default=False)
    field = models.BooleanField(default=False)

class User(AbstractUser):
    recent_video = models.ForeignKey(Video, on_delete=models.CASCADE,related_name='users_from_recent',null=True)
    painpart = models.ForeignKey(PainPart,on_delete=models.CASCADE,related_name="users_from_painpart",null=True)

    