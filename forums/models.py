from django.db import models 
from users.models import User

# 게시판
class Forum(models.Model):
    name = models.CharField(max_length=50,null=True)

# 게시글
class Post(models.Model): 
    title = models.CharField(max_length=300,null=False)
    content = models.CharField(max_length=10000,null=False) 
    num = models.CharField(max_length=4,null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)
    image = models.ImageField(upload_to='posts/',max_length=None,null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name = 'post_from_user',null=True)
    forum = models.ForeignKey(Forum,on_delete=models.CASCADE,related_name = 'post_from_forum',null=True)

# 게시글 좋아요
class PostLike(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name = 'postlike_from_post',null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name = 'postlike_from_user',null=True)

class Comment(models.Model):
    content = models.CharField(max_length = 200,null=False)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="comment_from_user",null=True)
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name="comment_from_post",null=True)