from rest_framework import serializers
from videos.models import BodyPart,Video
from users.models import VideoLike

class BodyPartSerializer(serializers.Serializer):
    class meta:
        model = BodyPart
        fields = ['id','neck','wrist','eye','waist','field']

class VideoSerializer(serializers.Serializer):
    videolikes_num = serializers.SerializerMethodField()

    bodypart = BodyPartSerializer()

    class Meta:
        model = Video
        fields = ['id','title','length','youtubelink','thumbnail','bodypart','videolikes_num']
    
    def get_videolikes_num(self,obj): # 동영상의 좋아요 개수 반환
        return VideoLike.objects.filter(video=obj).count()