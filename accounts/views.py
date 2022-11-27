from django.shortcuts import render
from .serializers import UserSerializer, SignupSerializer
from .models import User
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

import jwt, datetime

# 로그인은 Django REST Framework에서 제공되는 URL 이용

# 회원가입 커스터마이징
class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSerializer
    authentication_classes=[JWTAuthentication]
    permission_classes =[AllowAny]


