from .models import Blog
from .serializers import BlogSerializer
from rest_framework import viewsets
from .permissions import *
from rest_framework.permissions import IsAuthenticatedOrReadOnly

# Blog의 목록, detail 보여주기, 수정하기, 삭제하기 모두 가능
class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]    
    

    def perform_create(self, serializer):
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