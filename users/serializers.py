from rest_framework import serializers
from users.models import User,PainPart
from videos.serializers import VideoSerializer
from users.models import VideoLike

class PainPartSerializer(serializers.ModelSerializer): # 테스트 완료
    class Meta:
        model = PainPart
        fields = ['id','neck','wrist','eye','waist','field']

class UserSerializer(serializers.ModelSerializer): # 테스트 완료 / recent_video는 데이터 들어가는거 확인함. 나중에 최근에 본 비디오 데이터를 recent_video에 넣는 작업 필요
    userlikes_num = serializers.SerializerMethodField()
    
    recent_video = VideoSerializer()
    painpart = PainPartSerializer()

    class Meta:
        model = User
        fields = ['id','username','password','email','recent_video','painpart','userlikes_num']
        extra_kwargs = {'password':{'write_only':True}}

    def get_userlikes_num(self,obj): 
        return VideoLike.objects.filter(user=obj).count()

class VideoLikeSerializer(serializers.ModelSerializer): # 테스트 완료
      video = VideoSerializer()
      user = UserSerializer()

      class Meta:
          model = VideoLike
          fields = ['id','video','user']

