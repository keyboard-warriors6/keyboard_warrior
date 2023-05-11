from typing import Any, Dict
from django.shortcuts import render
from django.views.generic.base import View, TemplateView, RedirectView
from django.views.generic import ListView, DetailView
from products.models import Category, Product, Review, Review_imgs, Inquiry, Answer, Purchase, PurchaseItem


class ProductListView(ListView):
    model = Product
    # paginate_by = 12  # pagination이 필요한 경우 사용


class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'


    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        reviews = product.reviews.all()
        review_data = []
        for review in reviews:
            review_images = review.images.all()
            review_data.append({
                'review': review,
                'images': review_images,
            })
        context['reviews'] = review_data
        return context