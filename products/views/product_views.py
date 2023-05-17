import os
import sys
import requests
import json
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.db.models import ExpressionWrapper, FloatField, Count, F, Q
from django.views.generic import DeleteView, DetailView, ListView, TemplateView, View
from django.views.generic.edit import FormMixin, UpdateView
from products.forms import *
from products.models import *
from wordcloud import WordCloud 
import matplotlib.pyplot as plt
import numpy as np
from PIL import *


class ProductListView(TemplateView):
    template_name = 'products/product_list.html'

    def get_top_selling_products_by_brand(self, category):
        top_selling_product = Product.objects.filter(category__brand=category.brand).annotate(num_purchases=Count('purchaseitem')).order_by('-num_purchases')[:4]
        return top_selling_product
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # 구매량 많은 순으로 상위 12개 제품 가져오기
        most_purchased_products = Product.objects.annotate(num_purchases=Count('purchaseitem')).order_by('-num_purchases')[:12]
        context['most_purchased_products'] = most_purchased_products

        # 가성비 좋은 순으로 상위 5개 제품 가져오기
        affordable_products = Product.objects.annotate(affordability=ExpressionWrapper(
        Count('purchaseitem') / F('price'),
        output_field=FloatField()
        )).order_by('-affordability')[:12]
        context['affordable_products'] = affordable_products

        # 후기가 많은 순으로 상위 12개 제품 가져오기
        most_reviewed_products = Product.objects.annotate(num_reviews=Count('reviews')).order_by('-num_reviews')[:12]
        context['most_reviewed_products'] = most_reviewed_products

        # 브랜드별 판매량 상위 4개 상품 가져오기
        category_cox = Category.objects.filter(brand='콕스').first()
        if category_cox is not None:
            cox_selling_products = self.get_top_selling_products_by_brand(category_cox)
            context['cox_selling_products'] = cox_selling_products
        else:
            context['cox_selling_products'] = None

        category_corsair = Category.objects.filter(brand='커세어').first()
        if category_corsair is not None:
            corsair_selling_products = self.get_top_selling_products_by_brand(category_corsair)
            context['corsair_selling_products'] = corsair_selling_products
        else:
            context['corsair_selling_products'] = None

        category_leopold = Category.objects.filter(brand='레오폴드').first()
        if category_leopold is not None:
            leopold_selling_products = self.get_top_selling_products_by_brand(category_leopold)
            context['leopold_selling_products'] = leopold_selling_products
        else:
            context['leopold_selling_products'] = None

        # 가격이 낮은 순으로 상위 12개 제품 가져오기
        low_price_products = Product.objects.order_by('price')[:12]
        context['low_price_products'] = low_price_products
    
        return context
        
        
class ProductCategoryView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'products/category.html'  
    # paginate_by = 12  # pagination이 필요한 경우 사용

    def get_queryset(self):
        queryset = super().get_queryset()
        filter_option = self.request.GET.get('filter')
            # 필터 옵션에 따라 쿼리셋 필터링
        if filter_option == 'purchased':
            # 구매를 많이 한 순으로 정렬
            queryset = queryset.annotate(num_purchases=Count('purchaseitem')).order_by('-num_purchases')
        elif filter_option == 'popular':
            # 후기 많은 순으로 정렬
            queryset = queryset.annotate(num_reviews=Count('reviews')).order_by('-num_reviews')
        elif filter_option == 'affordable':
            # 가성비 좋은 순으로 정렬 (구매량/가격)
            queryset = queryset.annotate(affordability=ExpressionWrapper(
            Count('purchaseitem') / F('price'),
            output_field=FloatField())).order_by('-affordability')
        elif filter_option == 'low_price':
            # Sort by low price
            queryset = queryset.order_by('price')    

        brand = self.request.GET.get('brand')
        bluetooth = self.request.GET.get('bluetooth')
        switch = self.request.GET.get('switch')
        pressure = self.request.GET.get('pressure')
        tenkey = self.request.GET.get('tenkey')

        # 필터링 조건에 해당하는 Q 객체 생성
        filter_conditions = Q()

        if brand:
            filter_conditions &= Q(category__brand=brand)
        if bluetooth:
            filter_conditions &= Q(category__bluetooth=bluetooth)
        if switch:
            filter_conditions &= Q(category__switch=switch)
        if pressure:
            if pressure.endswith('~'):
                min_pressure = pressure[:-1].strip()
                filter_conditions &= Q(category__pressure__gte=min_pressure)
            else:
                min_pressure, max_pressure = pressure.split('~')
                filter_conditions &= Q(category__pressure__range=(min_pressure.strip(), max_pressure.strip()))
        if tenkey:
            filter_conditions &= Q(category__tenkey=tenkey)

        # 조건에 맞는 제품 리스트 반환
        return queryset.filter(filter_conditions)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        filter_option = self.request.GET.get('filter')

        if not filter_option:
            context['show_all'] = True  # 전체보기를 표시하기 위한 변수 설정
        
        return context
    

class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()

        reviews = product.reviews.all()
        review_data = []
        try:
            for review in reviews:
                review_images = review.images.all()
                review_data.append({
                    'review': review,
                    'images': review_images,
                })
        except:
            pass

        inquiries = product.inquiries.all()
        inquiry_data = []
        for inquiry in inquiries:
            try:
                inquiry_data.append({
                    'inquiry': inquiry,
                    'answer': inquiry.answer.all(),
                })
            except:
                inquiry_data.append({
                    'inquiry': inquiry,
                })

        context['category'] = product.category
        context['review_form'] = ReviewForm()
        context['inquiry_form'] = InquiryForm()
        context['answer_form'] = AnswerForm()
        context['review_image_form'] = ReviewImageForm() 
        context['reviews'] = review_data
        context['inquiries'] = inquiry_data
        return context
    

    def get_object(self, queryset=None):
        product_pk = self.kwargs.get('product_pk')
        product = self.model.objects.get(pk=product_pk)
        return product


class ProductSearchView(ListView):
    model = Product
    template_name = 'products/category.html'
    context_object_name = 'products'

    def get_queryset(self):
        query = self.request.GET.get('query')
        if query:
            return Product.objects.filter(name__icontains=query)
        return Product.objects.none()


class ProductCreateView(UserPassesTestMixin, PermissionRequiredMixin, FormMixin, TemplateView):
    model = Product
    second_model = Category
    form_class = ProductForm
    second_form_class = CategoryForm
    template_name = 'products/product_create.html'
    permission_required = 'products.add_product'
    raise_exception = True


    def test_func(self):
        return self.request.user.is_superuser


    def get_success_url(self):
        return reverse('products:product_detail', kwargs={'product_pk': self.model.objects.last().pk})


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_form'] = self.get_form(self.form_class)
        context['category_form'] = self.get_form(self.second_form_class)
        return context
    

    def post(self, request, *args, **kwargs):
        product_form = self.get_form(self.form_class)
        category_form = self.get_form(self.second_form_class)
        if product_form.is_valid() and category_form.is_valid():
            product = product_form.save(commit=False)
            category = category_form.save()
            product.category = category
            product.save()
            return self.form_valid(product_form)
        return self.form_invalid(product_form)


    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        product_form = self.get_form(form_class)
        category_form = self.get_form(self.second_form_class)
        return self.render_to_response(self.get_context_data(product_form=product_form, category_form=category_form))


    def form_valid(self, form):
        return super().form_valid(form)
    

    def form_invalid(self, form):
        return super().form_invalid(form)


class ProductUpdateView(UserPassesTestMixin, PermissionRequiredMixin, UpdateView):
    model = Product
    second_model = Category
    template_name = 'products/product_update.html'
    form_class = ProductForm
    second_form_class = CategoryForm
    permission_required = 'products.add_product'
    raise_exception = True
    pk_url_kwarg = 'product_pk'


    def test_func(self):
        return self.request.user.is_superuser


    def get_context_data(self, **kwargs):
        context = super(ProductUpdateView, self).get_context_data(**kwargs)
        product_pk = self.kwargs.get('product_pk', 0)
        product = self.model.objects.get(pk=product_pk)
        if 'product_form' not in context:
            context['product_form'] = self.form_class(instance=product)
        if 'category_form' not in context:
            context['category_form'] = self.second_form_class(instance=product.category)
        context['product_pk'] = product_pk
        return context


    def get_success_url(self):
        return reverse('products:product_detail', kwargs={'product_pk': self.kwargs.get('product_pk')})


    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        product_pk = kwargs['product_pk']
        product = self.model.objects.get(pk=product_pk)
        product_form = self.form_class(request.POST, request.FILES, instance=product)
        category_form = self.second_form_class(request.POST, instance=product.category)
        if product_form.is_valid() and category_form.is_valid():
            product_form.save()
            category_form.save()
            return redirect('products:product_detail', product_pk)
        else:
            return self.render_to_response(self.get_context_data(product_form=product_form, category_form=category_form))


class ProductDeleteView(UserPassesTestMixin, PermissionRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('products:product_list')
    pk_url_kwarg = 'product_pk'
    permission_required = 'products.add_product'
    raise_exception = True


    def test_func(self):
        return self.request.user.is_superuser


    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class ProductBookmarkView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        product_pk = kwargs['product_pk']
        product = Product.objects.get(pk=product_pk)
        if product.bookmark.filter(pk=request.user.pk).exists():
            product.bookmark.remove(request.user)
            bookmark = False
        else:
            product.bookmark.add(request.user)
            bookmark = True
        context = {
            'bookmark': bookmark,
        }
        return JsonResponse(context)
    

class KeyboardTrendView(TemplateView):
    template_name = 'products/keyboard_trend.html'  # 템플릿 파일 경로

    def get(self, request):
        trend_data1 = self.get_shopping_trend1()
        trend_data2 = self.get_shopping_trend2()
        trend_data_1 = trend_data1["results"]
        trend_data_2 = trend_data2["results"]
        result = {}
        for item in trend_data_1:
            title = item["title"]
            ratios = [data["ratio"] for data in item["data"]]
            total_ratio = sum(ratios)
            result[title] = total_ratio
        for item in trend_data_2:
            title = item["title"]
            ratios = [data["ratio"] for data in item["data"]]
            total_ratio = sum(ratios)
            result[title] = total_ratio
            wordcloud = WordCloud(width=1200, height=400).generate_from_frequencies(result)
            
            # 워드 클라우드 이미지를 파일로 저장
            image_path = '/wordcloud.png'
            wordcloud.to_file(image_path)
            
            # 템플릿 렌더링 및 응답 반환
            return render(request, 'products/keyboard_trend.html', {'wordcloud_image': image_path})
    
    def get_shopping_trend1(self):
        client_id = os.getenv('NAVER_CLIENT_ID') 
        client_secret = os.getenv('NAVER_CLIENT_SECRET')

        url = "https://openapi.naver.com/v1/datalab/shopping/category/keywords"
        headers = {
            "X-Naver-Client-Id": client_id,
            "X-Naver-Client-Secret": client_secret,
            "Content-Type": "application/json"
        }

        # 검색어 키워드 설정
        query = {
            "startDate": "2023-02-01",
            "endDate": "2023-04-30",
            "timeUnit": "month",
            "category": "50001204",
            "keyword": [
                {"name": "커세어", "param": ["커세어"]},
                {"name": "앱코", "param": ["앱코"]},
                {"name": "로지텍", "param": ["로지텍"]},
                {"name": "콕스", "param": ["콕스"]},
                {"name": "레오폴드", "param": ["레오폴드"]},
            ],
            "device": "",
            "ages": [],
            "gender": "",
        }

        response = requests.post(url, headers=headers, data=json.dumps(query))
        result = response.json()

        return result
    

    def get_shopping_trend2(self):
        client_id = os.getenv('NAVER_CLIENT_ID') 
        client_secret = os.getenv('NAVER_CLIENT_SECRET')

        url = "https://openapi.naver.com/v1/datalab/shopping/category/keywords"
        headers = {
            "X-Naver-Client-Id": client_id,
            "X-Naver-Client-Secret": client_secret,
            "Content-Type": "application/json"
        }

        # 검색어 키워드 설정
        query = {
            "startDate": "2023-02-01",
            "endDate": "2023-04-30",
            "timeUnit": "month",
            "category": "50001204",
            "keyword": [
                {"name": "리얼포스", "param": ["리얼포스"]},
                {"name": "덱", "param": ["덱"]},
                {"name": "듀가드", "param": ["듀가드"]},
                {"name": "키크론", "param": ["키크론"]},
                {"name": "씽크웨이", "param": ["씽크웨이"]},
            ],
            "device": "",
            "ages": [],
            "gender": "",
        }

        response = requests.post(url, headers=headers, data=json.dumps(query))
        result = response.json()

        return result
    

        # def get_shopping_trend1(self):
        # client_id = os.getenv('NAVER_CLIENT_ID') 
        # client_secret = os.getenv('NAVER_CLIENT_SECRET')

        # url = "https://openapi.naver.com/v1/datalab/shopping/category/keywords"
        # headers = {
        #     "X-Naver-Client-Id": client_id,
        #     "X-Naver-Client-Secret": client_secret,
        #     "Content-Type": "application/json"
        # }

        # # 검색어 키워드 설정
        # query = {
        #     "startDate": "2023-02-01",
        #     "endDate": "2023-04-30",
        #     "timeUnit": "month",
        #     "category": "50001204",
        #     "keyword": [
        #         {"name": "커세어", "param": ["커세어"]},
        #         {"name": "앱코", "param": ["앱코"]},
        #         {"name": "로지텍", "param": ["로지텍"]},
        #         {"name": "콕스", "param": ["콕스"]},
        #         {"name": "레오폴드", "param": ["레오폴드"]},
        #     ],
        #     "device": "",
        #     "ages": [],
        #     "gender": "",
        # }

        # response = requests.post(url, headers=headers, data=json.dumps(query))
        # result = response.json()

        # return result
    

        # def get_shopping_trend1(self):
        # client_id = os.getenv('NAVER_CLIENT_ID') 
        # client_secret = os.getenv('NAVER_CLIENT_SECRET')

        # url = "https://openapi.naver.com/v1/datalab/shopping/category/keywords"
        # headers = {
        #     "X-Naver-Client-Id": client_id,
        #     "X-Naver-Client-Secret": client_secret,
        #     "Content-Type": "application/json"
        # }

        # # 검색어 키워드 설정
        # query = {
        #     "startDate": "2023-02-01",
        #     "endDate": "2023-04-30",
        #     "timeUnit": "month",
        #     "category": "50001204",
        #     "keyword": [
        #         {"name": "커세어", "param": ["커세어"]},
        #         {"name": "앱코", "param": ["앱코"]},
        #         {"name": "로지텍", "param": ["로지텍"]},
        #         {"name": "콕스", "param": ["콕스"]},
        #         {"name": "레오폴드", "param": ["레오폴드"]},
        #     ],
        #     "device": "",
        #     "ages": [],
        #     "gender": "",
        # }

        # response = requests.post(url, headers=headers, data=json.dumps(query))
        # result = response.json()

        # return result
    


