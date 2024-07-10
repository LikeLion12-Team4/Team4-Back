from users import views
from rest_framework.routers import DefaultRouter
from django.urls import path


urlpatterns = [
    path('bodypart/',views.BodyPartListAPIView.as_view(),name = 'bodypart-list'),
    path('bodypart/<int:bodypart_id>',views.BodyPartRetrieveAPIView.as_view(),name = 'bodypart-retrieve'),
    path('videolike/',views.VideoLikeListAPIView.as_view(),name = 'videolike-list'),
    path('video_id/<int:video_id>/',views.VideoLikeRetrieveAPIView.as_view(),name = 'videolike-retrieve'),
    path('email/send/',views.send_email,name = "email-retrieve"),
    path('email/verify/',views.verify_email,name = "email-retrieve"),
]
router = DefaultRouter()
router.register(r'users',views.UserViewSet)
urlpatterns+=router.urls