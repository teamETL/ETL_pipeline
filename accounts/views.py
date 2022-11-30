from django.shortcuts import render
from .models import User
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import status
from rest_framework.response import Response

import jwt
from rest_framework.views import APIView
from .serializers import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.shortcuts import render, get_object_or_404
from myproject.settings import SECRET_KEY, ALGORITHM

from django.db.models import F, Sum, Count, Case, When


# 로그인은 Django REST Framework에서 제공되는 URL 이용
import logging
# logger = logging.getLogger('user')
# 회원가입 커스터마이징
class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSerializer
    authentication_classes=[JWTAuthentication]
    permission_classes =[AllowAny]

    def post(self, request):
        user = request.data

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        #logger.info(serializer.data[0]['id'])
        return Response(serializer.data, status=status.HTTP_201_CREATED)


#aggregation 관련 코드
class UserGenderStatisticsView(APIView):
    """
    유저의 남녀 수를 확인합니다.
    """
    permission_classes = [AllowAny]
    def get(self, request):
        male_cnt = User.objects.filter(gender="M").count()
        female_cnt = User.objects.filter(gender="F").count()
        return Response({"male_count": male_cnt, "female_count": female_cnt}, status=status.HTTP_200_OK)

class UserBirthStatisticsView(APIView):
    """
    유저의 출생일을 기준으로, 특정 세대에 속한 유저가 얼마나 되는지 확인합니다.
    """
    permission_classes = [AllowAny]
    def get(self, request):
        
        millennial_cnt = User.objects.filter(birth_date__range=["1981-01-01", "1995-12-31"]).count()
        genz_cnt = User.objects.filter(birth_date__range=["1996-01-01", "2012-12-31"]).count()
        alpha_cnt = User.objects.filter(birth_date__range=["2013-01-01", "2022-12-31"]).count()

        return Response({"밀레니얼세대(1981-95년생)":millennial_cnt, "Z세대(1996-2012년생)": genz_cnt, "알파세대(2013년생~)": alpha_cnt})


# class AuthView(APIView):
#     permission_classes =[AllowAny]
#     # 유저 정보 확인
#     def get(self, request):
#         try:
#             # access token을 decode 해서 유저 id 추출 => 유저 식별
#             access = request.COOKIES['access']
#             payload = jwt.decode(access, SECRET_KEY, algorithms=ALGORITHM)
#             pk = payload.get('user_id')
#             user = get_object_or_404(User, pk=pk)
#             serializer = LogInSerializer(instance=user)
#             return Response(serializer.data, status=status.HTTP_200_OK)

#         except(jwt.exceptions.ExpiredSignatureError):
#             # 토큰 만료 시 토큰 갱신
#             data = {'refresh': request.COOKIES.get('refresh', None)}
#             serializer = TokenRefreshSerializer(data=data)
#             if serializer.is_valid(raise_exception=True):
#                 access = serializer.data.get('access', None)
#                 refresh = serializer.data.get('refresh', None)
#                 payload = jwt.decode(access, SECRET_KEY, algorithms=['HS256'])
#                 pk = payload.get('user_id')
#                 user = get_object_or_404(User, pk=pk)
#                 serializer = LogInSerializer(instance=user)
#                 res = Response(serializer.data, status=status.HTTP_200_OK)
#                 res.set_cookie('access', access)
#                 res.set_cookie('refresh', refresh)
#                 return res
#             raise jwt.exceptions.InvalidTokenError

#         except(jwt.exceptions.InvalidTokenError):
#             # 사용 불가능한 토큰일 때
#             return Response(status=status.HTTP_400_BAD_REQUEST)

#     # 로그인
#     def post(self, request):
#     	# 유저 인증
#         user = authenticate(
#             email=request.data.get("email"), password=request.data.get("password")
#         )
#         # 이미 회원가입 된 유저일 때
#         if user is not None:
#             serializer = LogInSerializer(user)
#             # jwt 토큰 접근
#             token = TokenObtainPairSerializer.get_token(user)
#             refresh_token = str(token)
#             access_token = str(token.access_token)
#             res = Response(
#                 {
#                     "user": serializer.data,
#                     "message": "login success",
#                     "token": {
#                         "access": access_token,
#                         "refresh": refresh_token,
#                     },
#                 },
#                 status=status.HTTP_200_OK,
#             )
#             update_last_login(None, user)
#             # jwt 토큰 => 쿠키에 저장
#             res.set_cookie("access", access_token, httponly=True)
#             res.set_cookie("refresh", refresh_token, httponly=True)
#             return res
#         else:
#             return Response(status=status.HTTP_400_BAD_REQUEST)

#     # 로그아웃
#     def delete(self, request):
#         # 쿠키에 저장된 토큰 삭제 => 로그아웃 처리
#         response = Response({
#             "message": "Logout success"
#             }, status=status.HTTP_202_ACCEPTED)
#         response.delete_cookie("access")
#         response.delete_cookie("refresh")
#         return response

# class UserLogInView(generics.GenericAPIView):
#     queryset = User.objects.all()
#     serializer_class = LogInSerializer
#     permission_classes = [AllowAny]
    

#     def post(self, request):
#         serializer = LogInSerializer(data = request.data)
        
#         if not serializer.is_valid(raise_exception=True):
#             return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)
        
#         if serializer.validated_data['email'] == 'None':
#             return Response({"message": "fail"}, status=status.HTTP_200_OK)
#         response = {
#                 "access_token": serializer.validated_data['access_token']
#                 }
#         return Response(response, status=status.HTTP_200_OK)
