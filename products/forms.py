from django import forms
from .models import *


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
            
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['brand'].widget.attrs['class'] = 'product-create-form block mt-6 px-2.5 pb-2.5 pt-4 w-full text-sm text-gray-900 bg-white border-1 appearance-none peer'
        self.fields['brand'].widget.attrs['placeholder'] = " "
        self.fields['brand'].label = '브랜드명'
        self.fields['brand'].help_text = ''
        self.fields['bluetooth'].widget.attrs['class'] = 'product-create-form block mt-6 px-2.5 pb-2.5 pt-4 w-fulltext-gray-900 bg-white border-1 appearance-none peer'
        self.fields['switch'].widget.attrs['class'] = 'product-create-form block mt-6 px-2.5 pb-2.5 pt-4 w-full text-sm text-gray-900 bg-white border-1 appearance-none peer'
        self.fields['switch'].widget.attrs['placeholder'] = " "
        self.fields['switch'].label = '스위치 종류'
        self.fields['switch'].help_text = ''
        self.fields['pressure'].widget.attrs['class'] = 'product-create-form block mt-6 px-2.5 pb-2.5 pt-4 w-full text-sm text-gray-900 bg-white border-1 appearance-none peer'
        self.fields['pressure'].widget.attrs['placeholder'] = " "
        self.fields['pressure'].label = '키압(g)'
        self.fields['pressure'].help_text = '' 
        self.fields['tenkey'].widget.attrs['class'] = 'product-create-form block mt-6 px-2.5 pb-2.5 pt-4 w-fulltext-gray-900 bg-white border-1 appearance-none peer'

        
    """
    brand: 브랜드명
    bluetooth: True일 때 무선, False일 때 유선
    switch: 스위치의 종류
    pressure: 키압
    tenkey: True일 때 텐키리스, False일 때 풀배열
    """


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('name', 'content', 'product_img', 'price', 'discount_rate',)
        
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['name'].widget.attrs['class'] = 'product-create-form block mt-6 px-2.5 pb-2.5 pt-4 w-full text-sm text-gray-900 bg-white border-1 appearance-none peer'
        self.fields['name'].widget.attrs['placeholder'] = " "
        self.fields['name'].label = '제품명'
        self.fields['name'].help_text = ''
        self.fields['content'].widget.attrs['class'] = 'product-create-form block mt-6 px-2.5 pb-2.5 pt-4 w-full text-sm text-gray-900 bg-white border-1 appearance-none peer'
        self.fields['content'].widget.attrs['placeholder'] = " "
        self.fields['content'].label = '제품 설명'
        self.fields['content'].help_text = ''
        self.fields['product_img'].widget.attrs['class'] = 'product-create-form border'
        self.fields['product_img'].label = ""
        self.fields['price'].widget.attrs['class'] = 'product-create-form block mt-6 px-2.5 pb-2.5 pt-4 w-full text-sm text-gray-900 bg-white border-1 appearance-none peer'
        self.fields['price'].widget.attrs['placeholder'] = " "
        self.fields['price'].label = '제품 가격'
        self.fields['price'].help_text = ''
        self.fields['discount_rate'].widget.attrs['class'] = 'product-create-form block mt-6 px-2.5 pb-2.5 pt-4 w-full text-sm text-gray-900 bg-white border-1 appearance-none peer'
        self.fields['discount_rate'].widget.attrs['placeholder'] = " "
        self.fields['discount_rate'].label = '할인율(%)'
        self.fields['discount_rate'].help_text = '%빼고 정수 형태의 숫자로 적어주세요'

        
    """
    name: 제품명
    content: 제품 설명
    category: 제품의 특성에 따른 분류 모음 (아직 없음)
    product_img: 제품 사진
    price: 제품 가격
    discount_rate: 할인율
    """


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('content', 'rating',)


class ReviewImageForm(forms.ModelForm):
    img = forms.ImageField(widget=forms.FileInput)
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
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['content'].label = '문의 내용'


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ('content',)
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['content'].label = '답변 내용'


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