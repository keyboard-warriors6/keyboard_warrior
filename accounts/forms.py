from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ['username', 'email', 'profile_img', 'phone_number', 'user_address']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'signup-form block mt-6 px-2.5 pb-2.5 pt-4 w-full text-sm text-gray-900 bg-white border-1 appearance-none peer'
        self.fields['username'].widget.attrs['placeholder'] = " "
        self.fields['username'].label = '아이디'
        self.fields['username'].help_text = ''
        self.fields['email'].widget.attrs['class'] = 'signup-form block px-2.5 pb-2.5 pt-4 w-full text-sm text-gray-900 bg-white border-1 appearance-none peer'
        self.fields['email'].widget.attrs['placeholder'] = " "
        self.fields['profile_img'].widget.attrs['class'] = 'signup-form border'
        self.fields['profile_img'].label = ""
        self.fields['phone_number'].widget.attrs['class'] = 'signup-form block px-2.5 pb-2.5 pt-4 w-full text-sm text-gray-900 bg-white border-1 appearance-none peer'
        self.fields['phone_number'].widget.attrs['placeholder'] = " "
        self.fields['phone_number'].label = "휴대폰"
        self.fields['user_address'].widget.attrs['class'] = 'signup-form block px-2.5 pb-2.5 pt-4 w-full text-sm text-gray-900 bg-white border-1 appearance-none peer'
        self.fields['user_address'].widget.attrs['placeholder'] = " "
        self.fields['user_address'].label = "주소"
        self.fields['password1'].widget.attrs['class'] = 'signup-form block px-2.5 pb-2.5 pt-4 w-full text-sm text-gray-900 bg-white border-1 appearance-none peer'
        self.fields['password1'].widget.attrs['placeholder'] = " "
        self.fields['password1'].help_text = ''
        self.fields['password2'].widget.attrs['class'] = 'signup-form block px-2.5 pb-2.5 pt-4 w-full text-sm text-gray-900 bg-white border-1 appearance-none peer'
        self.fields['password2'].help_text = ''
        self.fields['password2'].widget.attrs['placeholder'] = " "


class CustomUserChangeForm(UserChangeForm):
    username = forms.CharField(disabled=True)

    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = ['username', 'email', 'profile_img', 'phone_number', 'user_address']
        
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'signup-form block mt-6 px-2.5 pb-2.5 pt-4 w-full text-sm text-gray-900 bg-white border-1 appearance-none peer'
        self.fields['username'].widget.attrs['placeholder'] = " "
        self.fields['username'].label = '아이디'
        self.fields['username'].help_text = ''
        self.fields['email'].widget.attrs['class'] = 'signup-form block px-2.5 pb-2.5 pt-4 w-full text-sm text-gray-900 bg-white border-1 appearance-none peer'
        self.fields['email'].widget.attrs['placeholder'] = " "
        self.fields['profile_img'].widget.attrs['class'] = 'signup-form border'
        self.fields['profile_img'].label = ""
        self.fields['phone_number'].widget.attrs['class'] = 'signup-form block px-2.5 pb-2.5 pt-4 w-full text-sm text-gray-900 bg-white border-1 appearance-none peer'
        self.fields['phone_number'].widget.attrs['placeholder'] = " "
        self.fields['phone_number'].label = "휴대폰"
        self.fields['user_address'].widget.attrs['class'] = 'signup-form block px-2.5 pb-2.5 pt-4 w-full text-sm text-gray-900 bg-white border-1 appearance-none peer'
        self.fields['user_address'].widget.attrs['placeholder'] = " "
        self.fields['user_address'].label = "주소"
