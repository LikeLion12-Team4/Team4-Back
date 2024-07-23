from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from forums.models import Forum,Post,PostLike,Comment
from forums.serializers import ForumSerializer,PostSerializer,PostLikeSerializer,CommentSerializer
from rest_framework.generics import CreateAPIView,DestroyAPIView,RetrieveAPIView,UpdateAPIView

# ==========================================================================================
#                                       Forum View
# ==========================================================================================

class ForumViewSet(viewsets.ModelViewSet): 
    queryset = Forum.objects.all()
    serializer_class = ForumSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'forum_id' 
    permission_classes = [IsAdminUser]

    def get_permissions(self):
        if self.action == "list":
            return [AllowAny()]
        return super().get_permissions()
    
# ==========================================================================================
#                                       Post View
# ==========================================================================================

class PostCreateRetrieveView(CreateAPIView,RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'forum_id' 
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            forum = Forum.objects.get(id = self.kwargs['forum_id'])
        except Forum.DoesNotExist:
            return Response({"error":"존재하지 않는 게시판입니다 !"},status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user,forum=forum)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def retrieve(self, request, *args, **kwargs):
        try:
            forum = Forum.objects.get(id=self.kwargs['forum_id'])
            post = Post.objects.filter(forum = forum)
        except Forum.DoesNotExist:
            return Response({"error":"게시판이 존재하지 않습니다 !"},status=status.HTTP_404_NOT_FOUND)
        serializer = PostSerializer(post,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class PostUpdateDestroyAPIView(UpdateAPIView,DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'post_id' 
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        try:
            post = Post.objects.get(id = self.kwargs['post_id'], user= request.user)
        except Post.DoesNotExist:
            return Response({"error":"본인의 게시글이 아니거나 없어진 게시글입니다!"},status=status.HTTP_401_UNAUTHORIZED)
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        try:
            post = Post.objects.get(id = self.kwargs['post_id'], user= request.user)
        except Post.DoesNotExist:
            return Response({"error":"본인의 게시글이 아니거나 없어진 게시글입니다!"},status=status.HTTP_401_UNAUTHORIZED)
        num = request.data.get('num')
        if num!=post.num:
            return Response({"error":"비밀번호가 틀립니다!"},status=status.HTTP_401_UNAUTHORIZED)
        return super().destroy(request, *args, **kwargs)

# ==========================================================================================
#                                       PostLike View
# ==========================================================================================
# 좋아요 생성, 삭제
class PostLikeCreateView(CreateAPIView):
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'post_id' 
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            post = Post.objects.get(id = self.kwargs['post_id'])
        except Post.DoesNotExist:
            return Response({"error":"게시글이 없습니다 !"},status=status.HTTP_404_NOT_FOUND)
        
        if PostLike.objects.filter(user=request.user,post=post).count()>0: # 이미 특정 동영상에 좋아요를 post한 사용자는 막음
            return Response({"error":"이미 좋아요를 눌렀습니다."},status=status.HTTP_400_BAD_REQUEST)
    
        postlike = PostLike.objects.create(user = request.user, post = post)
        postlike.save()
        serializer = self.get_serializer(postlike)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class PostLikeDeleteView(DestroyAPIView):
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'postlike_id' 
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        try:
            postlike = PostLike.objects.get(id = self.kwargs['postlike_id'], user= request.user)
        except PostLike.DoesNotExist:
            return Response({"error":"본인의 좋아요가 아니거나 없어진 좋아요 입니다! "},status=status.HTTP_401_UNAUTHORIZED)
        return super().destroy(request, *args, **kwargs)
  
# ==========================================================================================
#                                       Comment View
# ==========================================================================================

class CommentCreateRetrieveView(CreateAPIView,RetrieveAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'post_id' 
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            post = Post.objects.get(id = self.kwargs['post_id'])
        except Post.DoesNotExist:
            return Response({"error":"존재하지 않는 게시판입니다 !"},status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user,post=post)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def retrieve(self, request, *args, **kwargs):
        try:
            post = Post.objects.get(id=self.kwargs['post_id'])
            comment = Comment.objects.filter(post=post)
        except Post.DoesNotExist:
            return Response({"error":"게시글이 존재하지 않습니다 !"},status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(comment,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class CommentUpdateDestroyAPIView(UpdateAPIView,DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'comment_id' 
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        try:
            comment = Comment.objects.get(id = self.kwargs['comment_id'], user= request.user)
        except Comment.DoesNotExist:
            return Response({"error":"본인의 댓글이 아니거나 없어진 댓글입니다 !"},status=status.HTTP_401_UNAUTHORIZED)
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        try:
            comment = Comment.objects.get(id = self.kwargs['comment_id'], user= request.user)
        except Comment.DoesNotExist:
            return Response({"error":"본인의 댓글이 아니거나 없어진 댓글입니다 !"},status=status.HTTP_401_UNAUTHORIZED)
        return super().destroy(request, *args, **kwargs)

    