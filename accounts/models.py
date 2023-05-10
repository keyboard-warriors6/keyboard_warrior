from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import ugettext_lazy as _

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
    
    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if 'email' in extra_fields:
            del extra_fields['email']
        if 'phone_number' in extra_fields:
            del extra_fields['phone_number']
        if 'address' in extra_fields:
            del extra_fields['address']            

        return self.create_user(None, username, password, **extra_fields)


class User(AbstractUser):
    def accounts_image_path(instance, filename):
        return f'accounts/{instance.pk}/{filename}'
    
    profile_img = models.ImageField(upload_to=accounts_image_path, null=True, blank=True)
    phone_number = PhoneNumberField(default_region='KR', blank=True, null=True)
    user_address = models.CharField(max_length=255, blank=True)

    objects = CustomUserManager()

    def __str__(self):
        return self.username
    


