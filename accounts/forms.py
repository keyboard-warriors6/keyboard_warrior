from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ['username', 'email','password', 'profile_img', 'phone_number', 'user_address']


class CustomUserChangeForm(UserChangeForm):
    username = forms.CharField(disabled=True)

    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = ['username', 'email', 'profile_img', 'phone_number', 'user_address']