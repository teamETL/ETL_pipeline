from .models import User
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model




# 로그인 관련 시리얼라이져
class SignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required = True,
    ),
    password = serializers.CharField(
        required=True,
        write_only = True,
        style={'input_type': 'password'},
    )
    password2 = serializers.CharField(write_only = True, required=True, style={'input_type': 'password'})
    
    class Meta:
        model = User
        fields = ('email','nickname','gender','password','password2','name')
    
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({
                "password" : "비밀번호가 일치하지 않습니다."
            })
        
        return data

    def create(self, validated_data):
        user = User.objects.create(
            nickname = validated_data['nickname'],
            email = validated_data['email'],
            name = validated_data['name'],
            gender = validated_data['gender']
        )
        token = RefreshToken.for_user(user)
        user.set_password(validated_data['password'])
        user.refreshtoken = token
        user.save()
    
        return user

class UserSerializer(serializers.ModelSerializer):
    
        email = serializers.CharField(required=True, max_length=100, write_only=True,)
        password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})
                
        class Meta:
            model = get_user_model()
            fields = ('email', 'nickname','gender', 'password', 'name' )

    