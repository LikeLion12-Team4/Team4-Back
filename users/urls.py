from users import views
from rest_framework.routers import DefaultRouter
from django.urls import path

urlpatterns = [
    path('bodypart/',views.BodyPartListAPIView.as_view(),name = 'bodypart-list'),
    path('videolike/',views.VideoLikeListAPIView.as_view(),name = 'videolike-list'),
    path('video_id/<int:video_id>/',views.VideoLikeRetrieveAPIView.as_view(),name = 'videolike-retrieve'),
]

router = DefaultRouter()
router.register(r'users',views.UserViewSet)
urlpatterns+=router.urls