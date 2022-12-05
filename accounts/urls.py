from django.urls import path, include
from . import views
from rest_framework import urls
from customJWT.custom_jwt import CustomJWTObtainPairView
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
    # 회원가입
    path('signup/', views.UserCreateView.as_view(), name = 'sign-up'), 
    
    # 유저 리스트
    path('user_list/', views.UserListView.as_view(), name='user-list'),
       
    # 로그인 / 로그아웃
    path('login/', views.UserLogInView.as_view(), name='user-login'),

    # 회원 탈퇴 
    path('<int:pk>/withdraw/', views.UserWithdrawalView.as_view(), name='account-delete'),

    # 토큰 인증 view
    path('token/',TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_obtain_pair'),
    path('token/verify/',  TokenVerifyView.as_view(), name='token_verify'  ),

    # aggregation View
    path('gender-stats/', views.UserGenderStatisticsView.as_view(), name='gender-stats'),
    path('birth-stats/', views.UserBirthStatisticsView.as_view(), name='birth-stats'),
 ]