from rest_framework import serializers
from users.models import User,PainPart
from videos.serializers import VideoSerializer
from users.models import VideoLike

class PainPartSerializer(serializers.ModelSerializer): 
    class Meta:
        model = PainPart
        fields = ['id','painname']

class UserSerializer(serializers.ModelSerializer): 
    userlikes_num = serializers.SerializerMethodField()
    
    recent_video = VideoSerializer()
    painpart = PainPartSerializer()

    class Meta:
        model = User
        fields = ['id','username','password','email','recent_video','painpart','userlikes_num']
        extra_kwargs = {'password':{'write_only':True}}

    def get_userlikes_num(self,obj): 
        return VideoLike.objects.filter(user=obj).count()

class VideoLikeSerializer(serializers.ModelSerializer):
      video = VideoSerializer()
      user = UserSerializer()

      class Meta:
          model = VideoLike
          fields = ['id','video','user']

