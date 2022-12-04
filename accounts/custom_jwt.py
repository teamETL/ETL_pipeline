from datetime import datetime, timedelta

from django.conf import settings
from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView





# JWT 토큰 시리얼라이저 재정의
class CustomObtainPairSerializer(TokenObtainPairSerializer):
    """
    Simple JWT 토큰 오버라이딩
    """
    def validate(self, attrs):
        data = super(CustomObtainPairSerializer, self).validate(attrs)

        # 로그인 성공시 리턴할 데이터
        data['id'] = self.user.id
        data['email'] = self.user.email
        data['name'] = self.user.name
        data['nickname'] = self.user.nickname
        data['expires'] = datetime.now() + \
            settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"]

        return data

# JWT 토큰 생성 뷰 재정의
class CustomObtainPairView(TokenObtainPairView):
    """
    Simple JWT 토큰 뷰 재정의
    """
    # 토큰을 삭제하면 로그아웃 처리
    def delete(self, request, *arg, **kwargs):
        
        if 'drf_backend' in request.COOKES:
            response = HttpResponse(status=status.HTTP_200_OK)
            response.delete_cookie('drf_backend')
            return response

        else:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
