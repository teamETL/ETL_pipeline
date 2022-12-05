from datetime import datetime, timedelta

from django.conf import settings
from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication




# JWT 토큰 시리얼라이저 재정의
class CustomJWTObtainPairSerializer(TokenObtainPairSerializer):
    """
    Simple JWT 토큰 오버라이딩
    """
    def validate(self, attrs):
        data = super(CustomJWTObtainPairSerializer, self).validate(attrs)

        # 로그인 성공시 리턴할 데이터
        data['id'] = self.user.id
        data['email'] = self.user.email
        data['name'] = self.user.name
        data['nickname'] = self.user.nickname
        data['expires'] = datetime.now() + \
            settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"]

        return data
class CustomJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        raw_token = request.COOKIES.get('JWT', None)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token

# JWT 토큰 생성 뷰 재정의
class CustomJWTObtainPairView(TokenObtainPairView):
    """
    Simple JWT 토큰 뷰 재정의
    """
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code != 200:
            return response

        response.set_cookie(
            key = 'JWT',
            value = response.data['access'],
            max_age = 300,
            httponly = True,
            samesite = 'Lax'
        )
        return response
    # 토큰을 삭제하면 로그아웃 처리
    def delete(self, request, *arg, **kwargs):
        
        if 'JWT' in request.COOKES:
            response = HttpResponse(status=status.HTTP_200_OK)
            response.delete_cookie('JWT')
            return response

        else:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
