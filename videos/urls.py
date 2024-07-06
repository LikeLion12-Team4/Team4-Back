from videos import views
from rest_framework.routers import DefaultRouter
from django.urls import path

urlpatterns = [
]

router = DefaultRouter()
router.register(r'videos',views.VideoViewSet)
urlpatterns+=router.urls