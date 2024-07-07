from users import views
from rest_framework.routers import DefaultRouter
from django.urls import path


urlpatterns = [
    path('bodypart/',views.BodyPartListAPIView.as_view(),name = 'bodypart-list'),
    path('videolike/',views.VideoLikeListAPIView.as_view(),name = 'videolike-list'),
    path('video_id/<int:video_id>/',views.VideoLikeRetrieveAPIView.as_view(),name = 'videolike-retrieve'),
    #kakao
    path('kakao/login/', views.kakao_login, name='kakao_login'),
    path('kakao/callback/', views.kakao_callback, name='kakao_callback'),
    path('kakao/login/finish/', views.KaKaoLogin.as_view(),name='kakao_login_todjango'),
    #naver
    # path('naver/login', views.naver_login, name='naver_login'),
    # path('naver/callback/', views.naver_callback, name='naver_callback'),
    # path('naver/login/finish/', views.NaverLogin.as_view(), name='naver_login_todjango'),

]

router = DefaultRouter()
router.register(r'users',views.UserViewSet)
urlpatterns+=router.urls