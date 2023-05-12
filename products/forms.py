from django import forms
from .models import Category, Product, Review, Review_imgs, Inquiry, Answer, Purchase, PurchaseItem, Cart


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
        model = Review_imgs
        fields = ('img',)


class ReviewImageUpdateForm(forms.ModelForm):
    img = forms.ImageField(widget=forms.ClearableFileInput)
    class Meta:
        model = Review_imgs
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
    

# PurchaseItemFormSet = forms.models.inlineformset_factory(
#     Purchase,
#     PurchaseItem,
#     fields = ('cnt',),
#     extra = 1,
#     can_delete=False,
# )

class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ('cnt',)