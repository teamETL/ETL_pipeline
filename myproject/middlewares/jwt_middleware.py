from rest_framework_simplejwt.state import token_backend
from accounts.models import User
from django.conf import settings

class SecureJwtRequestMiddleware:
    def __init__(self, get_response):
        self.get_response=get_response

    
    def __call__(self, request):
        # HTTP 요청에서 httponly 쿠키를 찾는다.
        if 'drf_backend' in request.COOKIES:

            # 쿠키가 있으면 쿠키에서 JWT토큰을 가져온다.
            token_cookie = request.COOKIES['drf_backend']

            # Request header에 Jwt Token을 추가한다.
            request.META['HTTP_AUTHORIZATION'] = f"Bearer{token_cookie}"

            # 토큰에서 사용자 정보를 생성한다.
            payload = token_backend.decode(token_cookie, verify=True)
            request.user = User.objects.filter(id=payload['user_id']).first()

        # 다음 미들웨어에 받은 Request를 넘겨준다.
        response = self.get_response(request)

        return response

class SecureJwtResponseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # 요청 처리 후 response를 받는다
        response = self.get_response(request)

        # Token 요청에 따른 response인 경우
        if request.path_info.endswith("/user/token") and request.method =='POST' and hasattr(response, 'data'):
            
            # Simple JWT 토큰 응답인 경우
            if 'access' in response.data:
                # 토큰을 쿠키로 저장
                response.set_cookie(
                    key='drf_backend',
                    value=response.data['access'],
                    max_age=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds(),
                    httponly=True
                )
        
                # 토큰을 response에서 삭제
                response.data.pop('access')
                response.data.pop('refresh')
                response.content = response.render().rendered_content

        return response

        