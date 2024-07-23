from forums import views
from rest_framework.routers import DefaultRouter
from django.urls import path

urlpatterns = [
    path('post/<int:forum_id>/',views.PostCreateRetrieveView.as_view(),name = 'post-createretrieve'),
    path('post/retrieve/<int:post_id>/',views.PostUpdateDestroyAPIView.as_view(),name = 'post-updatedestory'),

    path('postlike/create/<int:post_id>/',views.PostLikeCreateView.as_view(),name = 'postlike-create'),
    path('postlike/<int:postlike_id>/',views.PostLikeDeleteView.as_view(),name = 'postlike-delete'),

    path('comment/<int:post_id>/',views.CommentCreateRetrieveView.as_view(),name = 'comment-createretrieve'),
    path('comment/retrieve/<int:comment_id>/',views.CommentUpdateDestroyAPIView.as_view(),name = 'comment-updatedestory'),

]

router = DefaultRouter()
router.register(r'forums',views.ForumViewSet)

urlpatterns+=router.urls