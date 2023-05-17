from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ['username', 'last_name', 'first_name', 'email', 'profile_img', 'phone_number', 'user_address']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'signup-form block mt-6 px-2.5 pb-2.5 pt-4 w-full text-sm text-gray-900 bg-white border-1 appearance-none focus:ring-0 invalid:[&:not(:placeholder-shown):not(:focus)]:border-red-500 peer'
        self.fields['username'].widget.attrs['pattern'] = '.{1,}'
        self.fields['username'].widget.attrs['placeholder'] = " "
        self.fields['username'].label = '아이디'
        self.fields['username'].help_text = ''

        self.fields['last_name'].widget.attrs['class'] = 'signup-form block px-2.5 pb-2.5 pt-4 w-full text-sm text-gray-900 bg-white border-1 appearance-none focus:ring-0 invalid:[&:not(:placeholder-shown):not(:focus)]:border-red-500 peer'
        self.fields['last_name'].widget.attrs['pattern'] = '.{1,}'
        self.fields['last_name'].widget.attrs['placeholder'] = " "
        self.fields['last_name'].label = '성'
        self.fields['last_name'].help_text = ''

        self.fields['first_name'].widget.attrs['class'] = 'signup-form block px-2.5 pb-2.5 pt-4 w-full text-sm text-gray-900 bg-white border-1 appearance-none focus:ring-0 invalid:[&:not(:placeholder-shown):not(:focus)]:border-red-500 peer'
        self.fields['first_name'].widget.attrs['pattern'] = '.{1,}'
        self.fields['first_name'].widget.attrs['placeholder'] = " "
        self.fields['first_name'].label = '이름'
        self.fields['first_name'].help_text = ''

        self.fields['email'].widget.attrs['class'] = 'signup-form block px-2.5 pb-2.5 pt-4 w-full text-sm text-gray-900 bg-white border-1 appearance-none focus:ring-0 invalid:[&:not(:placeholder-shown):not(:focus)]:border-red-500 peer'
        self.fields['email'].widget.attrs['pattern'] = '[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$'
        self.fields['email'].widget.attrs['placeholder'] = " "

        self.fields['profile_img'].widget.attrs['class'] = 'signup-form block w-full border text-sm text-gray-500 file:mr-4 file:py-1 file:px-4 file:border-0 file:text-sm file:font-semibold file:bg-[#99ccff] file:text-white hover:file:bg-[#99ccff]'
        self.fields['profile_img'].label = "프로필 사진"

        self.fields['phone_number'].widget.attrs['class'] = 'signup-form block px-2.5 pb-2.5 pt-4 w-full text-sm text-gray-900 bg-white border-1 appearance-none focus:ring-0 invalid:[&:not(:placeholder-shown):not(:focus)]:border-red-500 peer'
        self.fields['phone_number'].widget.attrs['pattern'] = '[0-9]{11}|^01([0|1|6|7|8|9])-?([0-9]{3,4})-?([0-9]{4})'
        self.fields['phone_number'].widget.attrs['placeholder'] = " "
        self.fields['phone_number'].label = "휴대폰"

        self.fields['user_address'].widget.attrs['class'] = 'signup-form block px-2.5 pb-2.5 pt-4 w-full text-sm text-gray-900 bg-white border-1 appearance-none focus:ring-0 peer'
        self.fields['user_address'].widget.attrs['placeholder'] = " "
        self.fields['user_address'].label = "주소"

        self.fields['password1'].widget.attrs['class'] = 'signup-form block px-2.5 pb-2.5 pt-4 w-full text-sm text-gray-900 bg-white border-1 appearance-none invalid:[&:not(:placeholder-shown):not(:focus)]:border-red-500 peer'
        self.fields['password1'].widget.attrs['pattern'] = '^(?=.*\d)(?=.*[a-zA-Z]).{8,}$'
        self.fields['password1'].widget.attrs['placeholder'] = " "
        self.fields['password1'].help_text = ''

        self.fields['password2'].widget.attrs['class'] = 'signup-form block px-2.5 pb-2.5 pt-4 w-full text-sm text-gray-900 bg-white border-1 appearance-none focus:ring-0 invalid:[&:not(:placeholder-shown):not(:focus)]:border-red-500 peer'
        self.fields['password2'].help_text = ''
        self.fields['password2'].widget.attrs['placeholder'] = " "


class CustomUserChangeForm(UserChangeForm):
    username = forms.CharField(disabled=True)


    class Meta(UserChangeForm.Meta):
        model = get_user_model()
        fields = ['username', 'email', 'profile_img', 'phone_number', 'user_address']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'signup-form block mt-6 px-2.5 pb-2.5 pt-4 w-full text-sm text-gray-900 bg-white border-1 appearance-none invalid:[&:not(:placeholder-shown):not(:focus)]:border-red-500 peer'
        self.fields['username'].widget.attrs['pattern'] = '.{1,}'
        self.fields['username'].widget.attrs['placeholder'] = " "
        self.fields['username'].label = '아이디'
        self.fields['username'].help_text = ''

        self.fields['email'].widget.attrs['class'] = 'signup-form block px-2.5 pb-2.5 pt-4 w-full text-sm text-gray-900 bg-white border-1 appearance-none invalid:[&:not(:placeholder-shown):not(:focus)]:border-red-500 peer'
        self.fields['email'].widget.attrs['pattern'] = '[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$'
        self.fields['email'].widget.attrs['placeholder'] = " "

        self.fields['profile_img'].widget.attrs['class'] = 'signup-form block w-full border text-sm text-gray-500 file:mr-4 file:py-1 file:px-4 file:border-0 file:text-sm file:font-semibold file:bg-[#99ccff] file:text-white hover:file:bg-[#99ccff]'
        self.fields['profile_img'].label = "프로필 사진"

        self.fields['phone_number'].widget.attrs['class'] = 'signup-form block px-2.5 pb-2.5 pt-4 w-full text-sm text-gray-900 bg-white border-1 appearance-none invalid:[&:not(:placeholder-shown):not(:focus)]:border-red-500 peer'
        self.fields['phone_number'].widget.attrs['pattern'] = '[0-9]{11}|^01([0|1|6|7|8|9])-?([0-9]{3,4})-?([0-9]{4})'
        self.fields['phone_number'].widget.attrs['placeholder'] = " "
        self.fields['phone_number'].label = "휴대폰"

        self.fields['user_address'].widget.attrs['class'] = 'signup-form block px-2.5 pb-2.5 pt-4 w-full text-sm text-gray-900 bg-white border-1 appearance-none peer'
        self.fields['user_address'].widget.attrs['placeholder'] = " "
        self.fields['user_address'].label = "주소"