from django.db import models
from django.conf import settings
from accounts.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator

class Blog(models.Model):

    # 1. 게시글의 id 값
    id = models.AutoField(primary_key=True, null=False, blank=False) 

    # 2. 제목
    title = models.CharField(max_length=100)

    # 3. 작성일
    created_at = models.DateTimeField(auto_now_add=True)

    # 4. 수정일
    updated_at = models.DateTimeField(auto_now=True)

    # 5. 작성자 CASCADE( 사용자 정보삭제 시 게시글도 같이 삭제하는 Option )
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)

    # 6. 본문
    body = models.TextField()

    # 7. 조회수 ( validator를 활용하여 최소값을 0으로 지정 )
    views = models.IntegerField(validators=[MinValueValidator(0)], default=0)


    class Meta:
        db_table = 'text' # 테이블명을 text 로 설정