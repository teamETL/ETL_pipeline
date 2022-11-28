from .models import User
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import update_last_login




# 회원가입 시리얼라이져
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
# 로그인 시리얼라이져 
class LogInSerializer(serializers.Serializer):
    email = serializers.EmailField(required = True, max_length=64, write_only=True ),
    password = serializers.CharField(required=True, style={'input_type': 'password'} )
    
    class Meta:
        model = User
        fields = ('email', 'password')
        
    def validate(self, data):
        email = data.get('email',None)
        password = data.get('password',None)

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)

            if not user.check_password(password):
                raise serializers.ValidationError('이메일과 비밀번호가 일치하지 않습니다.')
        
        else:
            raise serializers.ValidationError("존재하지 않는 이메일입니다. 해당 이메일이 맞는지 확인해주세요.")
        

        token = RefreshToken.for_user(user=user)
        data = {
            'email' : user.email,
            'refresh_token' : str(token),
            'access_token' : str(token.access_token)
        }
        update_last_login(None, user)

        return data
# class UserSerializer(serializers.ModelSerializer):
    
#         email = serializers.CharField(required=True, max_length=100, write_only=True,)
#         password = serializers.CharField(required=True, write_only=True, style={'input_type': 'password'})
                
#         class Meta:
#             model = get_user_model()
#             fields = ('email', 'nickname','gender', 'password', 'name' )

    