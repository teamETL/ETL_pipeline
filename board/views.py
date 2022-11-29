from .models import Blog
from .serializers import BlogSerializer
from rest_framework import viewsets
from .permissions import *
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.generics import *
from rest_framework.response import Response

from django.shortcuts import render

import logging
logger = logging.getLogger('my')

# Viewset을 활용한 게시판 기능.
# Blog의 목록, detail 보여주기, 수정하기, 삭제하기 모두 가능
# class BlogViewSet(viewsets.ModelViewSet):
#     queryset = Blog.objects.all()
#     serializer_class = BlogSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]    
    

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)


class BlogView(ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # 현재 요청한 유저를 작성자로 설정
        serializer.save(user=self.request.user)


class BlogDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.views += 1  # 조회수 1 증가
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)