from rest_framework import serializers
from videos.models import Video,BodyPart

class BodyPartSerializer(serializers.ModelSerializer): 
    class Meta:
        model = BodyPart
        fields = ['id','bodyname']
        
class VideoSerializer(serializers.ModelSerializer):
    videolikes_num = serializers.SerializerMethodField()
    bodypart = BodyPartSerializer(required=False)

    class Meta:
        model = Video
        fields = ['id','title','length','youtubelink','thumbnail','bodypart','videolikes_num']
    
    def get_videolikes_num(self,obj): # 동영상의 좋아요 개수 반환
        from users.models import VideoLike
        return VideoLike.objects.filter(video=obj).count()
