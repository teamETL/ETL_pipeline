from rest_framework import permissions
"""
Permission의 종류

1. AllowAny : 모든 요청에 대해 허가.
2. IsAuthenticated : 유저가 존재하고, 로그인 되어있을 경우 허가.
3. IsAdminUser : 유저가 존재하고, 관리자 계정일 경우에만 허가.
4. IsAuthentiactedOrReadOnly : 안전한 request Method 이거나 유저가 존재하고 로그인 되어 있을 경우에 허가.

"""
# 안전한 Methods 정의 : 수정, 삽입, 삭제 를 하지않아서 안전하다고 부른다.
SAFE_METHODS =('GET','HEAD','OPTIONS')

class IsUserOrReadonly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        
        # 조회 요청은 항상 누구나 볼수 있게 True

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user