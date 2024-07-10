from videos import views
from rest_framework.routers import DefaultRouter
from django.urls import path

urlpatterns = [
    path('webcam/',views.open_webcam,name = 'webcam'),
]

router = DefaultRouter()
router.register(r'videos',views.VideoViewSet)
urlpatterns+=router.urls