from django.contrib import admin
from django.forms import ModelForm
from .models import *


class CategoryAdminForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class ProductAdminForm(ModelForm):
    category = CategoryAdminForm()

    class Meta:
        model = Product
        fields = '__all__'


class ReviewImagesInline(admin.TabularInline):
    model = ReviewImages


class CartProductInline(admin.TabularInline):
    model = Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    inlines = [ReviewImagesInline]


admin.site.register(Category)
admin.site.register(Inquiry)
admin.site.register(Answer)
admin.site.register(Purchase)
admin.site.register(Cart)