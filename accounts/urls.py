from django.urls import path, include
from . import views
from rest_framework import urls
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

"""
http://localhost:8000/account/password/reset/
http://localhost:8000/account/password/reset/confirm/
http://localhost:8000/account/login/
http://localhost:8000/account/logout/
http://localhost:8000/account/user/
http://localhost:8000/account/password/change/
http://localhost:8000/accounttoken/verify/
http://localhost:8000/account/token/refresh/
"""
urlpatterns =[
    # 로그인 / 회원가입
    
    path('signup/', views.UserCreateView.as_view(), name = 'sign-up'), # 회원가입
    #path('auth/', views.AuthView.as_view(), name = 'auth'), # 로그인

    # # 토큰
    # path('token/', TokenObtainPairView.as_view()),
    # path('token/refresh/', TokenRefreshView.as_view()),
    # path('token/verify/',TokenVerifyView.as_view()),
    
    # 로그인 화면 기능
    path('api-auth/', include('rest_framework.urls')),

    #aggregation 관련 코드
    path('gender-stats/', views.UserGenderStatisticsView.as_view(), name='gender-stats'),
 ]