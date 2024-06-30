from rest_framework import serializers
from videos.models import BodyPart,Video
from users.models import VideoLike

class BodyPartSerializer(serializers.ModelSerializer): # 테스트 완료
    class Meta:
        model = BodyPart
        fields = ['id','neck','wrist','eye','waist','field']

class VideoSerializer(serializers.ModelSerializer): # 테스트 완료 / thumbnail 테스트 방법을 모르겠음..
    videolikes_num = serializers.SerializerMethodField()

    bodypart = BodyPartSerializer()

    class Meta:
        model = Video
        fields = ['id','title','length','youtubelink','thumbnail','bodypart','videolikes_num']
    
    def get_videolikes_num(self,obj): # 동영상의 좋아요 개수 반환, postman으로 test하기
        return VideoLike.objects.filter(video=obj).count()