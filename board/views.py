from .models import Blog
from .serializers import *
from rest_framework import viewsets
from .permissions import *
from rest_framework.permissions import *
from rest_framework.generics import *
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from rest_framework.views import APIView
import django_filters
from .hashing import get_hash, update_file, encrypt
from rest_framework_simplejwt.authentication import JWTAuthentication
import logging
from rest_framework.decorators import action


logger = logging.getLogger('user')

# Viewset을 활용한 게시판 기능.
# Blog의 목록, detail 보여주기, 수정하기, 삭제하기 모두 가능
# class BlogViewSet(viewsets.ModelViewSet):
#     queryset = Blog.objects.all()
#     serializer_class = BlogSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]    
    

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)
class BlogListView(ListAPIView):
    authentication_classes=[JWTAuthentication]
    
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    authentication_classes=[JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    # 필터 기능 추가
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ['user']



    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        
        #logger.info("GET content list success", extra ={'request':request,'user': request.user.pk})
        page = self.paginate_queryset(queryset)
        
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    
class BlogCreateView(CreateAPIView):
    authentication_classes=[JWTAuthentication]
    permission_classes =[IsAuthenticated]
    serializer_class = BlogSerializer
    http_method_names= ['get', 'head','post']

    def perform_create(self, serializer):
        # 현재 요청한 유저를 작성자로 설정
        serializer.save(user=self.request.user)
    def create(self, request, *args, **kwrags):
        self.http_method_names.append("GET")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        logger.info(
            "POST  content create success",
            extra={
                'request':request,
                'user_id': get_hash(get_hash(request.user.pk)), #hashing 함수 씌우기 #hashing 함수 씌우기
                'board_id': serializer.data['id']
            })
        update_file() #encrypted_log update
        
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        



class BlogDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    authentication_classes=[JWTAuthentication]
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    @action(
        detail=False,
        permission_classes=[AllowAny]        
    )
    def retrieve(self, request, *args, **kwargs):
        blog = self.get_object()
        blog.views += 1  # 조회수 1 증가
        blog.save()
        serializer = self.get_serializer(blog)
        #logger.info("GET Access Content Detail", extra={'request':request})
        return Response(serializer.data)     
       

    def update(self, request, *args, **kwargs):
        blog = self.get_object()
        partial = kwargs.pop('partial', False)
        
        # 수정 데이터 직렬화
        serializer = self.get_serializer(blog, data=request.data, partial=partial)

        # 데이터 유효성 검사
        serializer.is_valid(raise_exception=True)
        
        self.perform_update(serializer) # 글을 업데이트
        logger.info(
           "PUT content update success",
           extra={
                'request':request,
                'user_id': get_hash(get_hash(request.user.pk)),
                'board_id': serializer.data['id']
           })

        if getattr(blog, '_prefetched_objects_cache', None):
            blog._prefetched_objects_cache = {}
        update_file() #encrypted_log update
        
        return Response(serializer.data)

        # if serializer.is_valid():
        #     serializer.save() #UserSerializer의 유효성 검사를 한 뒤 DB에 저장
        #     logger.info("PUT Access Revise Board", extra={'request' : request})
        #     return Response(serializer.data, status=status.HTTP_201_CREATED) #client에게 JSON response 전달
        # else:
        #     logger.info("PUT Denied Revise Board", extra={'request' : request})
        #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        

    def destroy(self, request, *args, **kwargs):
        blog = self.get_object()
        serializer = self.get_serializer(blog)
        logger.info(
           "DELETE content success",
           extra={
                'request':request,
                'user_id': get_hash(get_hash(request.user.pk)),
                'board_id': serializer.data['id']
           })

        update_file() #encrypted_log update
        self.perform_destroy(blog)
        
        return Response(status=status.HTTP_204_NO_CONTENT)

class BlogStatisticsView(APIView):
    authentication_classes=[JWTAuthentication]    
    permission_classes = [AllowAny]
    def get(self, request):
        male_cnt = Blog.objects.filter(user__gender="M").count()
        female_cnt = Blog.objects.filter(user__gender="F").count()
        logger.info(request.__dict__['_user'])
        return Response({"Male":male_cnt, "Female": female_cnt}, status=status.HTTP_200_OK)

    # def post(self, request):
    #     user = request.GET.get('user')
    #     user_board = Blog.objects.filter(user__email=user).count()
    #     return Response({f"{user} 의 게시물 개수": user_board}, SAFE_METHODS=status.HTTP_200_OK)