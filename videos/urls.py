from videos import views
from rest_framework.routers import DefaultRouter
from django.urls import path

urlpatterns = [
    path('chatbot/', views.ChatbotView.as_view(), name='chatbot'),
]

router = DefaultRouter()
router.register(r'videos',views.VideoViewSet)
urlpatterns+=router.urls