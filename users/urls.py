from users import views
from rest_framework.routers import DefaultRouter
from django.urls import path


urlpatterns = [
    path('bodypart/',views.BodyPartListAPIView.as_view(),name = 'bodypart-list'),
    path('bodypart/<int:bodypart_id>/',views.delete_bodypart,name = 'bodypart-delete'),
    path('videolike/',views.VideoLikeListAPIView.as_view(),name = 'videolike-list'),
    path('video_id/<int:video_id>/',views.VideoLikeRetrieveAPIView.as_view(),name = 'videolike-retrieve'),
    path('email/send/',views.send_email,name = "email-send"),
    path('email/verify/',views.verify_email,name = "email-verify"),
    #kakao
    path("kakao/login/",views.kakao_login,name = "kakao-callback"),
    path("kakao/login/finish/",views.KakaoLoginView.as_view()),
    path("kakao/jwt/", views.kakao_jwt_view, name='kakao-jwt-view'),
    #naver
    path("naver/login/",views.naver_login,name = "naver-callback"),
    path("naver/login/finish/",views.NaverLoginView.as_view()),
    path("naver/jwt/", views.naver_jwt_view, name='naver-jwt-view'),

    path('postdata/',views.PoseDataView.as_view(),name='posedata'),
]
router = DefaultRouter()
router.register(r'users',views.UserViewSet)
urlpatterns+=router.urls