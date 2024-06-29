from django.db import models

# Create your models here.

class Hospital(models.Model):
    name=models.CharField(max_length=50,null=True)
    address=models.CharField(max_length=50,null=True)
    number=models.CharField(max_length=50,null=True)
    time=models.CharField(max_length=50,null=True)
    image=models.ImageField(upload_to='hospitals/', height_field=200, width_field=200, max_length=None,null=True) #이미지 없을 시 넣을 디폴트 이미지
    longitude=models.DecimalField(max_digits=10, decimal_places=6)
    latitude=models.DecimalField(max_digits=10, decimal_places=6)

class Lesson(models.Model):
    name=models.CharField(max_length=50,null=True)
    address=models.CharField(max_length=50,null=True)
    number=models.CharField(max_length=50,null=True)
    time=models.CharField(max_length=50,null=True)
    image=models.ImageField(upload_to='lessons/', height_field=200, width_field=200, max_length=None,null=True)
    longitude=models.DecimalField(max_digits=10, decimal_places=6)
    latitude=models.DecimalField(max_digits=10, decimal_places=6)



    
