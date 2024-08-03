import sys
import os
import django
# project_root = os.path.dirname(os.path.abspath(__file__)) + '/../'
# sys.path.append(project_root)
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
# django.setup()
from celery import shared_task
from firebase_admin import credentials, messaging, initialize_app
from django.utils import timezone

from alarms.models import Option,AlarmContent
from users.models import BodyPart
from videos.models import Video
from config.settings import HOST_NAME
# 서비스 계정 키 파일 경로
cred = credentials.Certificate("likelion12-4f281-firebase-adminsdk-68vuu-8f6a64002e.json")

# Firebase 초기화
initialize_app(cred)

@shared_task
def check_and_send_push_alarms():
    now = timezone.now()
    options = Option.objects.filter(is_alarm=True) # 알람을 설정해놓은 option
    for option in options:
        time = (now - option.last_push_time).total_seconds() / 60
        if time >= option.interval: # 알람 시간 되면 send_push_alarm
            send_push_alarm(option)
            option.last_push_time = now
            option.save()

def send_push_alarm(option):
    bodypart_list = option.owner.bodypart.all() if option.owner.bodypart is not None else BodyPart.objects.all()
    chosen_bodypart = bodypart_list.order_by("?").first()
    
    # content_list = AlarmContent.objects.filter(bodypart=chosen_bodypart)
    # video_list = Video.objects.filter(bodypart=chosen_bodypart)
    
    chosen_content = AlarmContent.objects.filter(bodypart=chosen_bodypart).order_by("?").first()
    chosen_video = Video.objects.filter(bodypart=chosen_bodypart).order_by("?").first()
    
    #fcm_token = "djRV1vbQuHOwmz9RdWgzRx:APA91bHZlFoY4UgxH6VlpySf9VFdQkMlbLRpk0OWdkmIr5h93js0Ln09Md3O8D1DXO2z9cPyit0segI8Mg7NNyS7JbL0wKXjYBukaFwlOEVGCYjaRu8RI07cMIVLssRSdMgte0Nk1yPC"
    fcm_token = option.fcm_token
    if fcm_token is None:
        print('No fcm token')
        return
    
    message = messaging.Message(
        data = {
            "video_title": chosen_video.title,
            "thumbnail": chosen_video.thumbnail,
            "url": chosen_video.youtubelink,
            "content_title": chosen_content.content,
            "content_image": chosen_content.image.url,
            "badge": 'media/pushes/304.png'
        },
        token=fcm_token
    )
    # 푸시 알림 메시지 전송
    response = messaging.send(message)
    print('Successfully sent message:', response)
