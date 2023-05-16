from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
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
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, is_active = True, is_staff=True, is_superuser=True, **extra_fields)
        user.set_password(password)
        user.save()
        return user


class User(AbstractUser):
    def accounts_image_path(instance, filename):
        return f'accounts/{instance.pk}/{filename}'


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