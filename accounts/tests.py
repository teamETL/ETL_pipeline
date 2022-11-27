import json
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User 
from .serializers import UserSerializer
import requests

class RegistrationTestCase(APITestCase):
    def setUp(self):
        self.url = "user/signup/"

    def test_registration(self):
        data = {"username": "testcase", "email": "test@localhost.app",
        "password1": "some_strong_psw", "password2": "some_strong_psw"}
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED) #if status code = 201, test success

class ProfileViewSetTestCase(APITestCase):  #수정중
    
    list_url = reverse("profile-list") #???
    
    API_ENDPOINT = "user/signup/"
    # data to be sent to api
    data = {'username': "davinci",
        'email':'test2@localhost.app',
        'password1':"very-strong-psw",
        'password2':"-very-strong-psw"}

    response = requests.post(url = API_ENDPOINT, data = data)
    resp_json = response.json() #parsed into dict
    jwt_access_token = resp_json["access_token"]
    jwt_refresh_token = resp_json["refresh_token"]

    def setup(self):
        self.user = User.objects.create_user(username="davinci", password="some-very-strong-psw") #이게 작동하는게 맞나...??
        # self.token = Token.objects.create(user=self.user)
        self.api_authentication()
    
    # def api_authentication(self):
    #     self.client.credentials(HTTP_AUTHORIZATION="Token "+self.token.key)
        
    # def test_profile_list_authenticated(self):
    #     response = self.client.get(self.list_url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    # def test_profile_list_un_authenticated(self):
    #     self.client.force_authenticate(user=None)
    #     response = self.client.get(self.list_url)
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    # def test_profile_detail_retrieve(self):
    #     response = self.client.get(reverse("profile-detail", kwargs={"pk":1}))
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data["user"], "davinci")
        
    # def test_profile_update_by_owner(self):
    #     response = self.client.put(reverse("profile-detail", kwargs={"pk":1}), {"city": "Anchiano", "bio": "Renaissance Genius"})
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(json.loads(response.content), {"id": 1, "user": "davinci", "bio": "Renaissance Genius", "city": "Anchiano", "avatar": None})
        
    # def test_profile_update_by_random_user(self):
    #     random_user = User.objects.create_user(username="random", password="psw123123123")
    #     self.client.force_authenticate(user=random_user)
    #     response = self.client.put(reverse("profile-detail", kwargs={"pk":1}), {"bio": "hacked!!"})
    #     self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)