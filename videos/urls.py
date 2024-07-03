from videos import views
from rest_framework.routers import DefaultRouter
from django.urls import path

urlpatterns = [
    path('bodypart/',views.BodyPartListAPIView.as_view(),name = 'bodypart-list'),
    path('<int:bodypart_id>/bodypart_id/',views.BodyPartRetrieveAPIView.as_view(),name = 'bodypart-retrieve'),
    path('',views.VideoListAPIView.as_view(),name = 'video-list'),
    path('<int:video_id>/video_id/',views.VideoRetrieveAPIView.as_view(),name = 'video-retrieve'),
]
