import json, os, requests, operator
import numpy as np
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.db.models import ExpressionWrapper, FloatField, Count, F, Q, Avg
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import DeleteView, DetailView, ListView, TemplateView, View
from django.views.generic.edit import FormMixin, UpdateView
from products.forms import *
from products.models import *
from PIL import Image
from wordcloud import WordCloud 
from matplotlib import font_manager

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

        # 구매량 많은 상위 12개 제품의 별점 평균
        # raw_rating = Review.objects.annotate(avg_rating=Avg('rating'))
        most_purchased_rating = Product.objects.filter(pk__in=most_purchased_products).annotate(avg_rating=Avg('reviews__rating'))
        context['most_purchased_rating'] = most_purchased_rating

        # 가성비 좋은 순으로 상위 5개 제품 가져오기
        affordable_products = Product.objects.annotate(affordability=ExpressionWrapper(
        Count('purchaseitem') / F('discounted_price'),
        output_field=FloatField()
        )).order_by('-affordability')[:12]
        context['affordable_products'] = affordable_products

        # 가성비 좋은 상위 5개 제품의 별점 평균
        affordable_rating = Product.objects.filter(pk__in=affordable_products).annotate(avg_rating=Avg('reviews__rating'))
        context['affordable_rating'] = affordable_rating

        # 후기가 많은 순으로 상위 12개 제품 가져오기
        most_reviewed_products = Product.objects.annotate(num_reviews=Count('reviews')).order_by('-num_reviews')[:12]
        context['most_reviewed_products'] = most_reviewed_products

        # 후기가 많은 상위 12개 제품의 별점 평균
        most_reviewed_rating = Product.objects.filter(pk__in=most_reviewed_products).annotate(avg_rating=Avg('reviews__rating'))
        context['most_reviewed_rating'] = most_reviewed_rating

        # 브랜드별 판매량 상위 4개 제품 및 별점 평균 가져오기
        category_cox = Category.objects.filter(brand='콕스').first()
        if category_cox is not None:
            cox_selling_products = self.get_top_selling_products_by_brand(category_cox)
            context['cox_selling_products'] = cox_selling_products
            cox_rating = Product.objects.filter(category__brand="콕스").annotate(avg_rating=Avg('reviews__rating'))
            context['cox_rating'] = cox_rating
        else:
            context['cox_selling_products'] = None
            context['cox_rating'] = None

        category_corsair = Category.objects.filter(brand='커세어').first()
        if category_corsair is not None:
            corsair_selling_products = self.get_top_selling_products_by_brand(category_corsair)
            context['corsair_selling_products'] = corsair_selling_products
            corsair_rating = Product.objects.filter(category__brand="커세어").annotate(avg_rating=Avg('reviews__rating'))
            context['corsair_rating'] = corsair_rating
        else:
            context['corsair_selling_products'] = None
            context['corsair_rating'] = None

        category_leopold = Category.objects.filter(brand='레오폴드').first()
        if category_leopold is not None:
            leopold_selling_products = self.get_top_selling_products_by_brand(category_leopold)
            context['leopold_selling_products'] = leopold_selling_products
            leopold_rating = Product.objects.filter(category__brand="레오폴드").annotate(avg_rating=Avg('reviews__rating'))
            context['leopold_rating'] = leopold_rating
        else:
            context['leopold_selling_products'] = None
            context['leopold_rating'] = None

        # 가격이 낮은 순으로 상위 12개 제품 가져오기
        low_price_products = Product.objects.order_by('discounted_price')[:12]
        context['low_price_products'] = low_price_products

        # 가격이 낮은 순으로 상위 12개 제품의 별점 평균
        low_price_rating = Product.objects.filter(pk__in=low_price_products).annotate(avg_rating=Avg('reviews__rating'))
        context['low_price_rating'] = low_price_rating

        return context
        

class ProductCategoryView(ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'products/category.html'  
    # paginate_by = 12  # pagination이 필요한 경우 사용
    
    def get_queryset(self):
        query = self.request.GET.get('query')
        queryset = super().get_queryset()
        filter_option = self.request.GET.get('filter')
        if query:
            queryset = queryset.filter(name__icontains=query)
            # 필터 옵션에 따라 쿼리셋 필터링
        if filter_option == 'purchased':
            # 구매를 많이 한 순으로 정렬
            queryset = queryset.annotate(num_purchases=Count('purchaseitem')).order_by('-num_purchases')
        elif filter_option == 'rating':
            queryset = queryset.annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating')     
        elif filter_option == 'popular':
            # 후기 많은 순으로 정렬
            queryset = queryset.annotate(num_reviews=Count('reviews')).order_by('-num_reviews')
        elif filter_option == 'affordable':
            # 가성비 좋은 순으로 정렬 (구매량/가격)
            queryset = queryset.annotate(affordability=ExpressionWrapper(
            Count('purchaseitem') / F('discounted_price'),
            output_field=FloatField())).order_by('-affordability')
        elif filter_option == 'low_price':
            # Sort by low price
            queryset = queryset.order_by('discounted_price')
        elif filter_option == 'all':
            queryset = queryset   

        brand = self.request.GET.getlist('brand')  # 다중 선택된 브랜드 값들을 배열로 받음
        bluetooth = self.request.GET.getlist('bluetooth')
        switch = self.request.GET.getlist('switch')
        pressure = self.request.GET.getlist('pressure')
        tenkey = self.request.GET.getlist('tenkey')

    # 필터링 조건에 해당하는 Q 객체 생성
        filter_conditions = Q()

        if brand:
            brand_conditions = Q()
            for b in brand:
                brand_conditions |= Q(category__brand=b)
            filter_conditions &= brand_conditions
        if bluetooth:
            bluetooth_conditions = Q()
            for b in bluetooth:
                bluetooth_conditions |= Q(category__bluetooth=b)
            filter_conditions &= bluetooth_conditions

        if switch:
            switch_conditions = Q()
            for s in switch:
                switch_conditions |= Q(category__switch=s)
            filter_conditions &= switch_conditions

        if pressure:
            pressure_conditions = Q()
            for pressure_range in pressure:
                pressure_range = pressure_range.strip()
                if pressure_range.endswith(','):
                    min_pressure = pressure_range[:-1].strip()
                    pressure_conditions |= Q(category__pressure__gte=min_pressure)
                else:
                    min_pressure, max_pressure = pressure_range.split(',')
                    pressure_conditions |= Q(category__pressure__range=(min_pressure.strip(), max_pressure.strip()))
            filter_conditions &= pressure_conditions

        if tenkey:
            tenkey_conditions = Q()
            for t in tenkey:
                tenkey_conditions |= Q(category__tenkey=t)
            filter_conditions &= tenkey_conditions

        # 조건에 맞는 제품 리스트 반환
        return queryset.filter(filter_conditions)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        ratingset = Product.objects.filter(pk__in=queryset).annotate(avg_rating=Avg('reviews__rating'))
        context['ratingset'] = ratingset
        
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
    

class KeyboardTrendView(UserPassesTestMixin, TemplateView):
    template_name = 'products/keyboard_trend.html'  # 템플릿 파일 경로
    raise_exception = True

    def test_func(self):
        return self.request.user.is_superuser

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
            result[title] = int(total_ratio)
        for item in trend_data_2:
            title = item["title"]
            ratios = [data["ratio"] for data in item["data"]]
            total_ratio = sum(ratios)
            result[title] = int(total_ratio)
        sorted_result = dict(sorted(result.items(), key=operator.itemgetter(1), reverse=True))
        image1_path = os.path.join(settings.BASE_DIR, 'static', 'img', 'trend.png')
        trend_mask=np.array(Image.open(image1_path))
        wordcloud = WordCloud(
                            background_color="grey",
                            colormap='Blues',
                            random_state=0,
                            min_font_size=20,
                            max_font_size=150,
                            prefer_horizontal=1,
                            collocations=False,
                            mask = trend_mask,
                            ).generate_from_frequencies(sorted_result)
        wordcloud = wordcloud.fit_words(sorted_result)

        font_path = os.path.join(settings.BASE_DIR, 'static', 'etc', 'NanumSquareNeo-eHv.ttf')
        fontprop = font_manager.FontProperties(fname=font_path)
        wordcloud.font_path = font_path
        # plt.imshow(wordcloud,interpolation='bilinear')
        # plt.axis('off')    
        image_path = 'static/img/word_cloud.png'
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
    

class BookmarkedProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'products/my_bookmark.html'
    context_object_name = 'bookmarked_products'
    
    def get_queryset(self):
        # 현재 로그인한 사용자의 북마크한 상품들만 조회합니다.
        return self.request.user.bookmark.all()