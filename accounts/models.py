from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import ugettext_lazy as _


class Level(models.Model):
    GRADE_CHOICES = [
        ('B', 'Bronze'), ('S', 'Silver'), ('G', 'Gold'), ('P', 'Platinum')
    ]
    grade = models.CharField(max_length=2, choices=GRADE_CHOICES)
    discount = models.IntegerField()


    def __str__(self):
        return self.get_grade_display()


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        if not username:
            raise ValueError(_('The Username field must be set'))
        
        email = self.normalize_email(email)     
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, password=None, email=None, **extra_fields):
        # extra_fields.setdefault('is_staff', True)
        # extra_fields.setdefault('is_superuser', True)
        # extra_fields.setdefault('is_active', True)

        # if not email:
        #     email = ''

        # if 'phone_number' in extra_fields:
        #     del extra_fields['phone_number']
        # if 'user_address' in extra_fields:
        #     del extra_fields['user_address']            

        # return self.create_user(email, username, password, **extra_fields)
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, is_active = True, is_staff=True, is_superuser=True, **extra_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractUser):
    def accounts_image_path(instance, filename):
        return f'accounts/{instance.pk}/{filename}'
    
    # email = models.EmailField(_('email address'), unique=True)
    # username = models.CharField(_('username'), max_length=150, unique=True)
    # date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    # is_active = models.BooleanField(_('active'), default=True)
    # is_staff = models.BooleanField(_('staff status'), default=False)
    
    profile_img = models.ImageField(upload_to=accounts_image_path, null=True, blank=True)
    phone_number = PhoneNumberField(region='KR', blank=True, null=True)
    user_address = models.CharField(max_length=255, blank=True)
    level = models.ForeignKey(Level, on_delete=models.SET_DEFAULT, default=1)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    def __str__(self):
        return self.username
    
    def get_full_name(self):
        return self.last_name + self.first_name

    def get_short_name(self):
        return self.first_name
    
    # 성, 이름 필드 자체를 지우려면 아래의 주석을 활성화시키면 됨.
    # first_name = None
    # last_name = None

    # class Meta:
    #     # db에서 first_name, last_name 컬럼 제거
    #     db_table = 'accounts_user'