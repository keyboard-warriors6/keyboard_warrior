from django import forms
from .models import *
from django.forms import inlineformset_factory, HiddenInput
from django.urls import reverse_lazy

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'content', 'product_img', 'price', 'discount_rate',)


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('content', 'rating',)


class ReviewImageForm(forms.ModelForm):
    img = forms.ImageField(widget=forms.FileInput(attrs={'multiple': True}))
    class Meta:
        model = ReviewImages
        fields = ('img',)


class ReviewImageUpdateForm(forms.ModelForm):
    img = forms.ImageField(widget=forms.ClearableFileInput)
    class Meta:
        model = ReviewImages
        fields = ('img',)


class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ('content',)


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('content',)


class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ('address',)
        

class CartForm(forms.ModelForm):
    cnt = forms.IntegerField(
        min_value=1,
        max_value=10,
        label='Count',
        initial=1,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Cart
        fields = ('cnt',)