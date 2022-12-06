from .models import User
from rest_framework import serializers, status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import *
from django.contrib.auth.models import update_last_login
from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError
import datetime
from django.conf import settings
from customJWT.custom_jwt import CustomJWTObtainPairSerializer


# 회원가입 시리얼라이져
class SignupSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(required = True),
    nickname = serializers.CharField(required = True),
    name = serializers.EmailField(required = True),
    password = serializers.CharField(
        required=True,
        write_only = True,
        style={'input_type': 'password'},
    )
    password2 = serializers.CharField(write_only = True, required=True, style={'input_type': 'password'})
    
    class Meta:
        model = User
        fields = ('email','nickname','gender','password','password2','name','birth_date')
    
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({
                "password" : "비밀번호가 일치하지 않습니다."
            })
        
        # if data['birth_date'] <= datetime.datetime.today():
        #     raise serializers.ValidationError({
        #         "birth_date" : "입력 하신 날짜가 올바르지 않습니다. 올바른 날짜를 입력해주세요"
        #     })
        return data

    def create(self, validated_data):
        user = User.objects.create(
            nickname = validated_data['nickname'],
            email = validated_data['email'],
            name = validated_data['name'],
            gender = validated_data['gender'],
            birth_date = validated_data['birth_date']
        )
        #token = RefreshToken.for_user(user)
        user.set_password(validated_data['password'])
        #user.refreshtoken = token
        user.save()
        
        return user

# 로그인 시리얼라이저
class LogInSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )

    def validate(self, data):
        user = authenticate(**data)
        if user:
            update_last_login(None, user)
            token = TokenObtainPairSerializer.get_token(user)
            refresh = str(token)
            access = str(token.access_token)
            data = {
                'email': user.email,
                'refresh': refresh,
                'access': access,
            }
            return data

        raise ValidationError({"detail": "No active account found with the given credentials"}, 'email')





        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
          model = User
          fields = '__all__'
    