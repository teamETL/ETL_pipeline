from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import datetime
class UserManager(BaseUserManager):
    # 일반 user 생성
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('must have user email')
        # if not gender:
        #     raise ValueError('must have user gender')
        # if not name:
        #     raise ValueError('must have user name')
        user = self.model(
            email = self.normalize_email(email),
            **extra_fields,
            # gender = gender,
            # nickname = nickname,
            # name = name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # 관리자 user 생성
    def create_superuser(self, email, password, **extra_fields):
        #extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_active', True)
        # if extra_fields.get('is_staff') is not True:
        #     raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_admin') is not True:
            raise ValueError(('Admin must have is_admin=True.'))
        user = self.create_user(
            email,
            password = password,
            **extra_fields
        )
        
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    
    # ( db에저장될이름, 선택사항 )
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    id = models.AutoField(primary_key=True)
    email = models.EmailField(default='', max_length=100, null=False, blank=False, unique=True)
    gender = models.CharField(default='', max_length=6, choices=GENDER_CHOICES, null=False, blank=False)
    birth_date =models.DateField(default=datetime.date.today, null=False, blank=False)
    nickname = models.CharField(default='', max_length=100, null=False, blank=False, unique=True)
    name = models.CharField(default='', max_length=100, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # User 모델의 필수 field
    is_active = models.BooleanField(default=True)    
    is_admin = models.BooleanField(default=False)
    
    # 헬퍼 클래스 사용
    objects = UserManager()

    # 사용자의 username field는 email 으로 설정
    USERNAME_FIELD = 'email'

    # 필수로 작성해야하는 field
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None): # True를 반환하여 권한이 있음을 알림
        return True

    def has_module_perms(self, app_label): # True를 반환하여 주어진 APP의 모델에 접근 가능하도록 함
        return True

    @property
    def is_staff(self): # True를 받아오면 장고의 관리자 화면에 로그인이 가능해짐.
        return self.is_admin
    
    class Meta:
        ordering =['id'] # 오름차순 정렬
        db_table = 'userinfo' # 테이블명을 userinfo로 설정