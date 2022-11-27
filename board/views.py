from .models import Blog
from .serializers import BlogSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from .permissions import IsUserOrReadonly
"""
viewsets.ModelViewSet

목록

mixins.ListModelMixin : list() 함수
특정 레코드

mixins.RetrieveModelMixin : retrieve() 함수
레코드 생성

mixins.CreateModelMixin : create() 함수
레코드 수정

mixins.UpdateModelMixin : update() 함수, partial_update() 함수
partial_update()

부분적인 필드값만 받아 수정이 가능하며 request method 중 Fetch 와 대응된다.

레코드 삭제

mixins.DestroyModelMixin : destroy() 함수
"""
# Blog의 목록, detail 보여주기, 수정하기, 삭제하기 모두 가능
class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [
        IsUserOrReadonly,
    ]

    def perfrom_create(self, serializer):
        serializer.save(user=self.request.user)


# blog_list = BlogViewSet.as_view({
#     'get' : 'list',
#     'post' : 'create',
# })
    
# blog_detail = BlogViewSet.as_view({
#     'get': 'retrieve',
#     'put': 'update',
#     'patch': 'partial_update',
#     'delete': 'destroy',
# })