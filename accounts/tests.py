import json
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from .models import User 
from .serializers import SignupSerializer, LogInSerializer
import requests

class TestUser(APITestCase):
    '''
        users app의 API 3개(회원가입, 로그인, 회원탈퇴) unit test
    '''
    def setUp(self):
        self.user = User(
            id       = 1,
            email    = "aaa@gmail.com",
            gender   = 'M',
            birth_date = '2000-01-01',
            nickname = "verynice",
            name     = "aaa",
            password = "pass_password",
            is_active = True,
            is_admin = False  # 일반유저          
        )
        self.user.save()
        
    # 회원가입
    def test_register_success(self):
        
        self.user_data = {
            "nickname"      : "verynice1",
            "password"      : "111222333",
            "password2"     : "111222333",
            "name"          : "홍길동",
            "email"         : "abc@gmail.com",
            "gender"        : "F",
            "birth_date"    : "1999-01-01",
            }

        self.register_url = "/user/signup/"
        self.response = self.client.post(self.register_url, data = self.user_data, format='json')
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    # 회원가입 중복아이디 체크 실패
    def test_register_id_ckeck_fail(self):
        
        self.user_data = {
            "nickname"      : "verynice1", 
            "password"      : "111222333",
            "password_check": "111222333",
            "name"          : "홍길동",
            "email"         : "abc@gmail.com", #중복이메일
            "gender"        : "F",
            "birth_date"    : "1999-01-02"
            }

        self.register_url = "/user/signup/"
        self.response = self.client.post(self.register_url, data = self.user_data, format='json')
        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)

    # 회원가입시 패스워드 확인 실패
    def test_register_password_check_fail(self):
        
        self.user_data = {
            "nickname"      : "verynice2", 
            "password"      : "111222333",
            "password_check": "111111111", #패스워드 확인 오류
            "name"          : "홍길동",
            "email"         : "abcd@gmail.com",
            "gender"        : "F",
            "birth_date"    : "1999-01-02"
            }

        self.register_url = "/user/signup/"
        self.response = self.client.post(self.register_url, data = self.user_data, format='json')
        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)

    # 로그인
    def test_login_success(self):
        self.login_url = "/user/api-auth/login/"
        data= {
                "email": "aaa@gmail.com",
                "password": "pass_password",
            }
        response= self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # 비밀번호 불일치
    def test_password_fail(self):
        self.login_url = "/user/api-auth/login/"
        data= {
                "username": "aaa@gmail.com",
                "password": "133",
            }
        response= self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        #self.assertEqual(response.json(), {'username': "{'detail': 'No active account found with the given credentials'}"})

    # 회원탈퇴
    # def test_withdraw_success(self):
    #     self.withdraw_url = f"/api/users/{self.user.id}/withdraw/"

    #     client = APIClient()
    #     client.force_authenticate(user=self.user)

    #     response = client.delete(self.withdraw_url, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)