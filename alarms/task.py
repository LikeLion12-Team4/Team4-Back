import random
from celery import shared_task
from firebase_admin import credentials, messaging, initialize_app
from django.utils import timezone

from .models import Option, AlarmContent
from users.models import BodyPart
from videos.models import Video
from config.settings import HOST_NAME
# 서비스 계정 키 파일 경로
cred = credentials.Certificate("team4-back-firebase-adminsdk-tqspp-91bf670255.json")

# Firebase 초기화
initialize_app(cred)

@shared_task
def check_and_send_push_alarms():
    now = timezone.now()
    options = Option.objects.filter(is_alarm=True)
    for option in options:
        time = (now - option.last_push_time).total_seconds() / 60
        if time >= option.interval:
            send_push_alarm(option)
            option.last_push_time = now
            option.save()

def send_push_alarm(option):
    bodypart_list = option.owner.badypart if option.owner.badypart is not None else BodyPart.objects.all()
    chosen_bodypart = random.choice(bodypart_list)
    content_list = AlarmContent.objects.filter(bodypart=chosen_bodypart)
    video_list = Video.objects.filter(bodypart=chosen_bodypart)
    
    chosen_content = random.choice(content_list)
    chosen_video = random.choice(video_list)
    
    fcm_token = option.fcm_token
    if fcm_token is None:
        print('No fcm token')
        return
    message = messaging.Message(
        notification = messaging.Notification(
            title="자세차렷 푸시 알림",
            body=chosen_content.content
        ),
        data = {
            "video_title,": chosen_video.title,
            "thumbnail": chosen_video.thumbnail,
            "url": chosen_video.youtubelink
        },
        webpush=messaging.WebpushConfig(
            notification=messaging.WebpushNotification(
                icon=HOST_NAME + chosen_content.image.url
            ),
        ),
        token=fcm_token
    )
    # 푸시 알림 메시지 전송
    response = messaging.send(message)
    print('Successfully sent message:', response)