from django import forms
from .models import *


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
        fields = ('address', 'purchase_items')
        # 추가
        widgets = {'purchase_items': forms.CheckboxSelectMultiple}

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        # 장바구니에 있는 상품 필터링
        cart_items = Cart.objects.filter(user=user)
        self.fields['purchase_items'].queryset = Product.objects.filter(id__in=cart_items.values('product__id'))

        # 상세 페이지에서 선택한 상품 필터링
        product_id = self.initial.get('product_id')
        if product_id:
            product = Product.objects.get(id=product_id)
            self.fields['purchase_items'].queryset = Product.objects.filter(id=product.id)

    purchase_items = forms.ModelMultipleChoiceField(queryset=Product.objects.none(), required=True)


# PurchaseItemFormSet = forms.models.inlineformset_factory(
#     Purchase,
#     PurchaseItem,
#     fields = ('cnt',),
#     extra = 1,
#     can_delete=False,
# )

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