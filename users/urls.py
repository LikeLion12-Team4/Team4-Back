from users import views
from rest_framework.routers import DefaultRouter
from django.urls import path

urlpatterns = [
    path('users/',views.PainPartListAPIView.as_view(),name = 'painpart-list'),
    path('users/<int:painpart_id>/painpart_id/',views.PainPartRetrieveAPIView.as_view(),name = 'painpart-retrieve'),
    path('users/<int:video_id>/videolike_id/',views.VideoLikeListAPIView.as_view(),name = 'video-list'),
]

router = DefaultRouter()
router.register(r'users',views.UserViewSet)
urlpatterns+=router.urls