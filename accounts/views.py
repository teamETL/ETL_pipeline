from .models import User
from rest_framework import generics, status
from rest_framework.permissions import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response



# 회원가입 뷰
class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSerializer
    permission_classes =[AllowAny]

    def post(self, request):
        user = request.data

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# 로그인 화면
class UserLogInView(generics.GenericAPIView):
    permission_classes =[AllowAny]
    serializer_class = LogInSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            
            email = serializer.validated_data['email']
            
            # 토큰 검증
            access_token = serializer.validated_data['access']
            refresh_token = serializer.validated_data['refresh']
            res = Response(
                {
                    "email": email,
                    "token": {
                        "refresh": refresh_token,
                        "access": access_token,
                    },
                },
                status=status.HTTP_200_OK,
            ) 

            # 쿠키데이터 저장
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)

            return res

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# 유저 리스트, 관리자만 접근 가능
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSerializer
    permission_classes =[IsAdminUser]



# 탈퇴 기능 뷰
class UserWithdrawalView(generics.DestroyAPIView):
    authentication_classes=[JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer


# aggregation 관련 코드
class UserGenderStatisticsView(APIView):
    """
    유저의 남녀 수를 확인합니다.
    """
    permission_classes = [AllowAny]
    def get(self, request):
        male_cnt = User.objects.filter(gender="M").count()
        female_cnt = User.objects.filter(gender="F").count()
        return Response({"male_count": male_cnt, "female_count": female_cnt}, status=status.HTTP_200_OK)

class UserBirthStatisticsView(APIView):
    """
    유저의 출생일을 기준으로, 특정 세대에 속한 유저가 얼마나 되는지 확인합니다.
    """
    permission_classes = [AllowAny]
    def get(self, request):
        
        millennial_cnt = User.objects.filter(birth_date__range=["1981-01-01", "1995-12-31"]).count()
        genz_cnt = User.objects.filter(birth_date__range=["1996-01-01", "2012-12-31"]).count()
        alpha_cnt = User.objects.filter(birth_date__range=["2013-01-01", "2022-12-31"]).count()

        return Response({"밀레니얼세대(1981-95년생)":millennial_cnt, "Z세대(1996-2012년생)": genz_cnt, "알파세대(2013년생~)": alpha_cnt})

