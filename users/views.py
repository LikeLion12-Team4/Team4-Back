from users.models import User,PainPart,VideoLike
from users.serializers import UserSerializer,PainPartSerializer,VideoLikeSerializer
from videos.models import Video

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,
    ListCreateAPIView
)
from django.contrib.auth.hashers import check_password

#from users.permissions import IsOwner

# ==========================================================================================
#                                   PainPart View 
# ==========================================================================================

class PainPartRetrieveAPIView(RetrieveUpdateDestroyAPIView): # 특정 아픈부위 수정
    queryset = PainPart.objects.all()
    serializer_class = PainPartSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'painpart_id'
    #permission_classes = [IsOwnerOrReadOnly]

class PainPartListAPIView(ListCreateAPIView): # 아픈부위 생성
    queryset = PainPart.objects.all()
    serializer_class = PainPartSerializer
    lookup_field = 'id'
    #permission_class = [IsOwnerOrReadOnly]

# ==========================================================================================
#                                       User View
# ==========================================================================================

class UserViewSet(viewsets.ModelViewSet): 
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'painpart_id' 
    #permission_classes = [IsOwner] 

    # 로그인
    @action(methods=['POST'],detail = False, url_path='login',url_name='user-login')
    def login(self,request): 
        username = request.data.get('username')
        password = request.data.get('password')
        user = User.objects.get(username = username) 
        if not check_password(password,user.password): 
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        token = RefreshToken.for_user(user) 
        serializer = UserSerializer(user) 
        return Response(
            status=status.HTTP_200_OK,
            data={
                "token":str(token.access_token), 
                "user":serializer.data,
            }
        )
    
    # 현재 로그인 중인 회원정보 보기
    @action(methods=['GET'],detail = False, url_path='user',url_name='user-info')
    def get_user_info(self,request): 
        if request.user.is_authenticated:
            serializer = UserSerializer(request.user)
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    # 회원가입 -> username, password, email 중복 체크 하기
    @action(methods=['POST'],detail=True,url_path='join',url_name='user-join')
    def join(self,request,painpart_id):
        try: # 특정 아픈부위 찾기
            painpart = PainPart.objects.get(id = painpart_id)
        except PainPart.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        fullname = request.data.get('fullname')
            
        if User.objects.filter(username=username).count()>0:
            return Response({"error":"username already existed"},status=status.HTTP_401_UNAUTHORIZED)
        if User.objects.filter(email=email).count()>0:
            return Response({"error":"email already existed"},status=status.HTTP_401_UNAUTHORIZED)
        for check_user in User.objects.all():
            if check_password(password,check_user.password):
                return Response({"error":"password already existed"},status=status.HTTP_401_UNAUTHORIZED)

        # django.db.utils.IntegrityError: UNIQUE constraint failed: users_user.username
        user = User.objects.create_user(username =username,
                                        password=password,
                                        email = email,
                                        fullname = fullname,
                                        painpart=painpart)
        serializer = UserSerializer(user)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
    # 회원탈퇴 ( 로그인한 회원만 탈퇴 )
    @action(methods=['DELETE'],detail = False, url_path='quit',url_name='user-quit')
    def quit(self, request):
        if request.user.is_authenticated:
            instance = request.user
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_401_UNAUTHORIZED)
    
    # 아이디 찾기
    @action(methods=['GET'],detail = False, url_path='find_id',url_name='user-findid')
    def find_username(self,request):
        fullname = request.data.get('fullname')
        email = request.data.get('email')
        try:
            user = User.objects.get(fullname=fullname,email=email)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    # 비밀번호 찾기
    @action(methods=['GET'],detail = False, url_path='find_pwd',url_name='user-findpwd')
    def find_username(self,request):
        username = request.data.get('username')
        fullname = request.data.get('fullname')
        email = request.data.get('email')
        try:
            user = User.objects.get(fullname=fullname,email=email,username = username)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return Response(serializer.data,status=status.HTTP_200_OK)



# ==========================================================================================
#                                       VideoLike View
# ==========================================================================================

class VideoLikeListAPIView(ListCreateAPIView):
    queryset = VideoLike.objects.all()
    serializer_class = VideoLikeSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'video_id'
    #permission_class = [IsOwnerOrReadOnly]

    def create(self, request, *args, **kwargs): 
        if VideoLike.objects.filter(user=request.user).count()>0: # 이미 특정 동영상에 좋아요를 post한 사용자는 막음
            return Response({"error":"you already posted videolike this video"},status=status.HTTP_400_BAD_REQUEST)
        try: # 특정 비디오 찾기
            video = Video.objects.get(id = self.kwargs['video_id'])
        except Video.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        videolike = VideoLike.objects.create(user = request.user, video=video)
        serializer = VideoLikeSerializer(videolike)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        
