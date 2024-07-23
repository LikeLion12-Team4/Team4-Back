from rest_framework import serializers
from forums.models import Forum,Post,PostLike,Comment
from users.serializers import UserSerializer

class ForumSerializer(serializers.ModelSerializer):
    class Meta:
        model = Forum
        fields = ['id','name']

class PostSerializer(serializers.ModelSerializer):
    postlikes_num = serializers.SerializerMethodField()
    comments_num = serializers.SerializerMethodField()
    user = UserSerializer(required=False)
    forum = ForumSerializer(required=False)

    class Meta:
        model = Post
        fields = ['id','title','content','num','created_at','updated_at','image','user','forum','postlikes_num','comments_num']
    
    def get_postlikes_num(self,obj):
        return PostLike.objects.filter(post=obj).count()
    
    def get_comments_num(self,obj):
        return Comment.objects.filter(post=obj).count()
    

class PostLikeSerializer(serializers.ModelSerializer):
    post = PostSerializer()
    user = UserSerializer()

    class Meta:
        model = PostLike
        fields = ['id','post','user']

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=False)
    post = PostSerializer(required=False)
    
    class Meta:
        model = Comment
        fields = ['id','content','created_at','user','post']
