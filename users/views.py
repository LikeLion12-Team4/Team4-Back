from users.models import User,BodyPart,VideoLike,Email
from users.serializers import UserSerializer,BodyPartSerializer,VideoLikeSerializer,EmailSerializer
from videos.models import Video
from alarms.models import Option

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action,api_view,permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
    CreateAPIView,
    ListCreateAPIView
)
from rest_framework.permissions import IsAuthenticated,AllowAny,IsAdminUser
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail

from random import randint
import re
#from users.permissions import IsOwner

# ==========================================================================================
#                                       BodyPart View 
# ==========================================================================================

class BodyPartListAPIView(ListCreateAPIView): # 아픈부위 생성, 아픈 부위가 추가 되지 않는 이상 사용안함
    queryset = BodyPart.objects.all()
    serializer_class = BodyPartSerializer
    lookup_field = 'id'
    permission_classes = [IsAdminUser]


@api_view(['DELETE']) 
@permission_classes([IsAdminUser])
def delete_bodypart(request,bodypart_id): # 아픈부위 삭제
    try:
        bodypart = BodyPart.objects.get(id=bodypart_id)
    except BodyPart.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    bodypart.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

# ==========================================================================================
#                                       User View
# ==========================================================================================

class UserViewSet(viewsets.ModelViewSet): 
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'user_id' 
    permission_classes = [AllowAny] 
    
    def get_permissions(self):
        if self.action == "get_user_info" or self.action == "survey" or self.action == "quit" or self.action == "reset_pwd" or self.action == "reset_id":
            return [IsAuthenticated()]
        elif self.action == "list" or self.action == "retrieve" or self.action=="destroy":
            return [IsAdminUser()]
        return super().get_permissions()
    
    # 로그인
    @action(methods=['POST'],detail = False, url_path='login',url_name='user-login')
    def login(self,request): 
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            user = User.objects.get(username = username)
        except User.DoesNotExist:
            return Response({"error":"계정이 없습니다."},status=status.HTTP_404_NOT_FOUND)
        
        if not check_password(password,user.password): 
            return Response({"error":"wrong information"},status=status.HTTP_401_UNAUTHORIZED)
        
        token = RefreshToken.for_user(user)  # 특정 함수를 실행하고 다음 실행은 로그인된 상태로 하게 하려면 token을 줘야함
        serializer = self.get_serializer(user) 
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
        serializer = self.get_serializer(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    # 회원가입 ( 회원가입 후에 바로 설문조사 해야 함 bodypart 데이터를 넣기 위해, 테스트 할 때 이메일 인증부터 받고 오기 )
    @action(methods=['POST'],detail=False,url_path='join',url_name='user-join')
    def join(self,request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        fullname = request.data.get('fullname')

        if self.id_valid_input(username):
            return Response({"error":"아이디는 2~10자의 한글이나 영문만 사용 가능합니다."},status=status.HTTP_401_UNAUTHORIZED)
        if self.pwd_valid_input(password):
            return Response({"error":"비밀번호는 8~15자의 영문, 숫자, 특수문자 2가지 이상 조합으로 사용 가능합니다."},status=status.HTTP_401_UNAUTHORIZED)

        # username, password, email 중복 체크
        if User.objects.filter(username=username).count()>0:
            return Response({"error":"이미 존재하는 아이디입니다."},status=status.HTTP_401_UNAUTHORIZED)
        if User.objects.filter(email=email).count()>0:
            return Response({"error":"이미 존재하는 이메일입니다."},status=status.HTTP_401_UNAUTHORIZED)
        
        try: # 이전에 이메일 인증을 하고 와야함
            email_model = Email.objects.get(email=email)
        except Email.DoesNotExist:
            return Response({"error":"이메일 인증을 받지 않았습니다."},status=status.HTTP_401_UNAUTHORIZED)
        
        if not email_model.is_verified: # 이메일 인증안했으면 막힘
            return Response({"error":"이메일 인증을 받지 않았습니다."},status=status.HTTP_401_UNAUTHORIZED)
        

        # 수정하기
        user = User.objects.create_user(username =username,
                                        password=password,
                                        email = email,
                                        fullname = fullname,
                                        )
        user.save()
        token = RefreshToken.for_user(user)
        serializer = self.get_serializer(user)
        email_model.delete()

        # Option
        Option.objects.create(owner = user)

        return Response(
            status=status.HTTP_201_CREATED,
            data={
                "token":str(token.access_token), 
                "user":serializer.data,
            }
        )
    
    # 설문조사 - user 아픈 부위 넣기 ( 회원가입 후에 바로 이루어짐, 로그인 한 상태로 이루어져야 함 ), 회원가입 후에 바로 로그인이 되도록 어케 함?
    @action(methods=['PUT'],detail=False,url_path='survey',url_name='user-survey') 
    def survey(self,request):
        query = request.data.get('bodypart') 
        bodypart_list = query.split(',') # request.data가 목,어깨,눈 형식일 때
        #bodypart_list = [int(x) for x in query.split(',')] #request.data 형태가 1,2,3 숫자일 때

        for bp in BodyPart.objects.filter(user=request.user): # bodypart 객체에서 user를 삭제 -> 추후에 수정을 위해
            bp.user.remove(request.user)
        
        for bp in BodyPart.objects.all(): # bodypart 객체에 user 추가
            for bodyname in bodypart_list:
                if bp.bodyname == bodyname:
                    bp.user.add(request.user)
        
        # user 객체에 bodypart 추가
        bodypart = BodyPart.objects.filter(user=request.user)
        request.user.bodypart.set(bodypart)
        serializer = UserSerializer(request.user)
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
    # 회원탈퇴 ( 로그인한 회원만 탈퇴 )
    @action(methods=['DELETE'],detail = False, url_path='quit',url_name='user-quit')
    def quit(self, request):
        instance = request.user
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    # 아이디 찾기
    @action(methods=['POST'],detail = False, url_path='find_id',url_name='user-findid')
    def find_id(self,request):
        fullname = request.data.get('fullname')
        email = request.data.get('email')
        
        if User.objects.filter(email=email).count()==0: # 이메일이 존재하지 않다면  
            return Response({"error":"이메일이 존재하지 않습니다"},status=status.HTTP_401_UNAUTHORIZED)
        elif User.objects.filter(email=email,fullname=fullname).count()==0:
            return Response({"error":"이메일과 일치하는 실명이 아닙니다"},status=status.HTTP_401_UNAUTHORIZED)
        
        try: # 이전에 이메일 인증을 하고 와야함
            email_model = Email.objects.get(email=email)
        except Email.DoesNotExist:
            return Response({"error":"이메일 인증을 받지 않았습니다."},status=status.HTTP_401_UNAUTHORIZED)
    
        if not email_model.is_verified:
            return Response({"error":"이메일 인증을 받지 않았습니다."},status=status.HTTP_401_UNAUTHORIZED)
        
        email_model.delete()
        user = User.objects.get(email=email,fullname=fullname)
        serializer = UserSerializer(user)
        
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    # 비밀번호 찾기
    @action(methods=['POST'],detail = False, url_path='find_pwd',url_name='user-findpwd')
    def find_pwd(self,request):
        username = request.data.get('username')
        fullname = request.data.get('fullname')
        email = request.data.get('email')

        if User.objects.filter(username=username).count()==0:
            return Response({"error":"아이디가 존재하지 않습니다 !"},status=status.HTTP_401_UNAUTHORIZED)
        elif User.objects.filter(email=email,username=username).count()==0:
            return Response({"error":"아이디와 일치하는 이메일이 아닙니다!"},status=status.HTTP_401_UNAUTHORIZED)
        elif User.objects.filter(email=email,username=username, fullname = fullname).count()==0:
            return Response({"error":"이메일과 아이디와 일치하는 실명이 아닙니다 !"},status=status.HTTP_401_UNAUTHORIZED)

        try: # 이전에 이메일 인증을 하고 와야함
            email_model = Email.objects.get(email=email)
        except Email.DoesNotExist:
            return Response({"error":"이메일 인증을 받지 않았습니다."},status=status.HTTP_401_UNAUTHORIZED)
        
        if not email_model.is_verified:
            return Response({"error":"이메일 인증을 받지 않았습니다."},status=status.HTTP_401_UNAUTHORIZED)
        
        email_model.delete()
        user = User.objects.get(username=username,email=email)
        serializer = UserSerializer(user)
        token = RefreshToken.for_user(user)
        return Response(
            status=status.HTTP_202_ACCEPTED,
            data={
                "token":str(token.access_token), 
                "user":serializer.data,
            }
        )
    
    # 아이디 재설정
    @action(methods=['PUT'],detail = False, url_path='reset_id',url_name='user-findid')
    def reset_id(self,request):
        print("!!")
        username = request.data.get('username')
        if self.id_valid_input(username):
            return Response({"error":"아이디는 4~12자의 숫자나 영문만 사용 가능합니다."},status=status.HTTP_401_UNAUTHORIZED)
        if User.objects.filter(username=username).count()>0:
            return Response({"error":"이미 존재하는 아이디입니다."},status=status.HTTP_401_UNAUTHORIZED)

        request.user.username = username
        request.user.save()
        serializer = self.get_serializer(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    # 비밀번호 재설정 ( 비밀번호 찾기 화면에서 이메일 인증을 했으면 로그인이 되도록 )
    @action(methods=['PUT'],detail = False, url_path='reset_pwd',url_name='user-findpwd')
    def reset_pwd(self,request):
        password = request.data.get('password')
        if self.pwd_valid_input(password):
            return Response({"error":"비밀번호는 8~15자의 영문, 숫자, 특수문자 2가지 이상 조합으로 사용 가능합니다."},status=status.HTTP_401_UNAUTHORIZED)
            
        re_password = request.data.get('re_password')
        if password != re_password:
            return Response({"error":"비밀번호가 다릅니다."},status=status.HTTP_406_NOT_ACCEPTABLE)

        request.user.set_password(password)
        request.user.save()
        serializer = self.get_serializer(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    # 이메일 인증번호 확인 -> 이메일 모델을 만들어서 해결
    @action(methods=['PUT'],detail=False,url_path='verify',url_name='email-verify')
    def email_verify(self,request):
        email = request.data.get('email')
        verify = request.data.get('verify')

        try: # 이전에 이메일 인증을 하고 와야함
            email_model = Email.objects.get(email=email)
        except Email.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if verify == email_model.verify_num:
            email_model.is_verified = True
            email_model.save()
            return Response({"성공":"인증번호를 확인하였습니다."},status=status.HTTP_202_ACCEPTED)
        else:
            return Response({"오류":"인증번호가 올바르지 않습니다."},status=status.HTTP_406_NOT_ACCEPTABLE)
        
    # id 조건 판단
    def id_valid_input(self,user_input): 
        pattern = r'^[a-zA-Z0-9]{4,12}$'
        return re.match(pattern, user_input) is None
    
    # 비밀번호 조건 판단
    def pwd_valid_input(self, user_input): 
        pattern = r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,15}$|^(?=.*\d)(?=.*[@$!%*?&])[\d@$!%*?&]{8,15}$|^(?=.*[A-Za-z])(?=.*[@$!%*?&])[A-Za-z@$!%*?&]{8,15}$|^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,15}$'
        return re.match(pattern, user_input) is None
    
# ==========================================================================================
#                                         Email FBV
# ========================================================================================== 

@api_view(['POST'])
def send_email(request):
    random_num = f"{randint(0,999999):06}" 
    subject = "자세차렷 인증 이메일 입니다."
    message = f'이메일 인증 코드는 < {random_num} > 입니다.'
    from_email = "likelion12@naver.com"
    recipient_list = [request.data.get('email')]

    email = Email.objects.filter(email = recipient_list[0])
    email.delete()

    email = Email.objects.create(verify_num = random_num,email=recipient_list[0])
    email.save()

    try:
        send_mail(subject=subject,message=message,from_email=from_email,recipient_list=recipient_list,fail_silently=False)
        return Response(status=status.HTTP_200_OK)
    except Exception as e: # 서버 오류 시 예외 처리
        return Response({"error": "Email send error"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

@api_view(['POST'])
def verify_email(request):
    email = request.data.get('email')
    verify = request.data.get('verify')

    try: # 이전에 이메일 인증을 하고 와야함
        email_model = Email.objects.get(email=email)
    except Email.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if verify == email_model.verify_num:
        email_model.is_verified = True
        email_model.save()
        return Response({"성공":"인증번호를 확인하였습니다."},status=status.HTTP_202_ACCEPTED)
    else:
        return Response({"오류":"인증번호가 올바르지 않습니다."},status=status.HTTP_406_NOT_ACCEPTABLE)

# ==========================================================================================
#                                       VideoLike View
# ========================================================================================== 
class VideoLikeListAPIView(ListAPIView):
    queryset = VideoLike.objects.all()
    serializer_class = VideoLikeSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

    # 좋아요 누른 동영상 보기
    def list(self, request, *args, **kwargs):
        videolike = VideoLike.objects.filter(user=request.user)
        videolikeserializer = self.get_serializer(videolike,many=True)
        return Response(videolikeserializer.data,status=status.HTTP_200_OK)

# 동영상 좋아요를 접근하기 위해 동영상 id 사용
class VideoLikeRetrieveAPIView(RetrieveUpdateDestroyAPIView,CreateAPIView): 
    queryset = VideoLike.objects.all()
    serializer_class = VideoLikeSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'video_id' # 동영상 id로 동영상 좋아요를 접근함
    permission_classes = [IsAuthenticated]

    # 동영상 좋아요 삭제 ( 로그인 해야함 )
    def destroy(self, request, *args, **kwargs):
        try: 
            video = Video.objects.get(id = self.kwargs['video_id'])
        except Video.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            videolike = VideoLike.objects.get(user=request.user,video=video)
        except VideoLike.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        self.perform_destroy(videolike)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    # 동영상 좋아요 post
    def create(self, request, *args, **kwargs):
        try: 
            video = Video.objects.get(id = self.kwargs['video_id'])
        except Video.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        if VideoLike.objects.filter(user=request.user,video=video).count()>0: # 이미 특정 동영상에 좋아요를 post한 사용자는 막음
            return Response({"error":"이미 좋아요를 눌렀습니다."},status=status.HTTP_400_BAD_REQUEST)
    
        videolike = VideoLike.objects.create(user = request.user, video=video)
        videolike.save()
        serializer = self.get_serializer(videolike)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# ==========================================================================================
#                                       Kakao
# ========================================================================================== 
from django.conf import settings
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.shortcuts import redirect

from .models import User
from .serializers import UserSerializer

import requests

BASE_URL = 'http://3.37.18.8:8000/'
LOCAL_BASE_URL='http://127.0.0.1:8000/'
KAKAO_CALLBACK_URI = BASE_URL + 'kakao/login/finish/'
NAVER_CALLBACK_URI = BASE_URL + 'naver/login/finish/'
KAKA0_LOCAL_URI=LOCAL_BASE_URL+'html/pages/social-sign-up.html'
import logging
state=getattr(settings,'STATE')
KAKAO_REST_API_KEY= getattr(settings, 'KAKAO_REST_API_KEY')
KAKAO_SECRET_KEY=getattr(settings, 'KAKAO_SECRET_KEY')
NAVER_REST_API_KEY= getattr(settings, 'SOCIAL_AUTH_NAVER_CLIENT_ID')
NAVER_SECRET_KEY=getattr(settings, 'SOCIAL_AUTH_NAVER_SECRET')

def kakao_login(request):
    return redirect(
        f"https://kauth.kakao.com/oauth/authorize?client_id={KAKAO_REST_API_KEY}&redirect_uri={KAKA0_LOCAL_URI}&response_type=code"
    )

class KakaoLoginView(APIView):
    def post(self, request, *args, **kwargs):
        code = request.data.get("code")
        if not code:
            return Response(
                {"error": "Code is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        # 카카오 인가코드를 사용해 access_token 획득
        token_res = requests.post(
            "https://kauth.kakao.com/oauth/token",
            data={
                "grant_type": "authorization_code",
                "client_id": KAKAO_REST_API_KEY,
                "client_secret": KAKAO_SECRET_KEY,
                "redirect_uri": KAKA0_LOCAL_URI,
                "code": code,
            },
        )

        if token_res.status_code != 200:
            print(token_res)
            return Response(
                {"error": "Failed to obtain access token"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        token_json = token_res.json()
        access_token = token_json.get("access_token")
        return Response({'access_token':access_token}, status=status.HTTP_200_OK)
    
@api_view(['POST'])
def kakao_jwt_view(request):
    access_token = request.data.get('access_token')
    # 카카오 access_token으로부터 사용자 정보 획득
    headers = {"Authorization": f"Bearer {access_token}"}
    profile_res = requests.get("https://kapi.kakao.com/v2/user/me", headers=headers)

    if profile_res.status_code != 200:
        print(profile_res)
        return Response(
            {"error": "Failed to obtain user information"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    profile_json = profile_res.json()

    username = profile_json.get("id")
    fullname = profile_json.get("properties")["nickname"]
    email = profile_json.get("kakao_account")["email"]

    user, created = User.objects.get_or_create(
        email=email,
        defaults={
            "username": f"{username}",
            "fullname": f"{fullname}",
        },
    )

    # 사용자에 대한 토큰 생성
    refresh = RefreshToken.for_user(user)
    data = {
        "access_token": str(refresh.access_token),
        "refresh_token": str(refresh),
        "user_info": {
            "username": user.username,
            "email": user.email,
            "fullname": user.fullname,
            "is_created": created,
        },
    }

    return Response(data, status=status.HTTP_200_OK)
# ==========================================================================================
#                                       Naver 
# ========================================================================================== 
# 네이버 로그인 창
def naver_login(request):
    client_id = getattr(settings, 'SOCIAL_AUTH_NAVER_CLIENT_ID')
    return redirect(f"https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id={NAVER_REST_API_KEY}&state=STATE_STRING&redirect_uri={NAVER_CALLBACK_URI}")

class NaverLoginView(APIView):
    def post(self, request, *args, **kwargs):
        code = request.query_params.get("code")
        if not code:
            return Response(
                {"error": "Code is required"}, status=status.HTTP_400_BAD_REQUEST
            )
        
        token_request = requests.get(f"https://nid.naver.com/oauth2.0/token?grant_type=authorization_code&client_id={NAVER_REST_API_KEY}&client_secret={NAVER_SECRET_KEY}&code={code}&state={state}")
        token_response_json = token_request.json()

        error = token_response_json.get("error", None)
        if error is not None:
            raise Exception(error)

        access_token = token_response_json.get("access_token")
        print("cc",access_token)
        #access token으로 네이버 프로필 요청
        profile_request = requests.post(
        "https://openapi.naver.com/v1/nid/me",
        headers={"Authorization": f"Bearer {access_token}"},
        )
        profile_json = profile_request.json()
        print("Dd",profile_json.get("response"))
    
        email = profile_json.get("response").get("email")
        username = profile_json.get("response").get("id")
        fullname = profile_json.get("response").get("name")

        user, created = User.objects.get_or_create(
            email= email,
            defaults={
                "username": f"{username}",
                "fullname": f"{fullname}",
            },
        )

        # 사용자에 대한 토큰 생성
        refresh = RefreshToken.for_user(user)
        data = {
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
            "user_info": {
                "username": user.username,
                "email": user.email,
                "fullname": user.fullname,
                "is_created": created,
            },
        }

        return Response(data, status=status.HTTP_200_OK)
    def get(self, request, *args, **kwargs):
        code = request.query_params.get("code")
        if not code:
            return Response(
                {"error": "Code is required"}, status=status.HTTP_400_BAD_REQUEST
            )
        
        token_request = requests.get(f"https://nid.naver.com/oauth2.0/token?grant_type=authorization_code&client_id={NAVER_REST_API_KEY}&client_secret={NAVER_SECRET_KEY}&code={code}&state={state}")
        token_response_json = token_request.json()

        error = token_response_json.get("error", None)
        if error is not None:
            raise Exception(error)

        access_token = token_response_json.get("access_token")
        print("cc",access_token)
        #access token으로 네이버 프로필 요청
        profile_request = requests.post(
        "https://openapi.naver.com/v1/nid/me",
        headers={"Authorization": f"Bearer {access_token}"},
        )
        profile_json = profile_request.json()

    
        email = profile_json.get("response").get("email")
        username = profile_json.get("response").get("id")
        fullname = profile_json.get("response").get("name")

        user, created = User.objects.get_or_create(
            email= email,
            defaults={
                "username": f"{username}",
                "fullname": f"{fullname}",
            },
        )

        # 사용자에 대한 토큰 생성
        refresh = RefreshToken.for_user(user)
        data = {
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
            "user_info": {
                "username": user.username,
                "email": user.email,
                "fullname": user.fullname,
                "is_created": created,
            },
        }

        return Response(data, status=status.HTTP_200_OK)