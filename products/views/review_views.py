from django.http import JsonResponse, Http404, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from django.views.generic.edit import ModelFormMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from products.models import *
from products.forms import *


class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    second_model = ReviewImages
    form_class = ReviewForm
    second_form_class = ReviewImageForm
    template_name = 'products/product_detail.html'

    def get_success_url(self):
        return reverse('products:product_detail', args=(self.object.product.pk,))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review_form'] = self.get_form(self.form_class)
        context['review_image_form'] = self.get_form(self.second_form_class)
        return context
    
    def post(self, request, *args, **kwargs):
        review_form = self.get_form(self.form_class)
        review_image_form = self.get_form(self.second_form_class)
        if review_form.is_valid() and review_image_form.is_valid():
            product = get_object_or_404(Product, pk=self.kwargs['product_pk'])
            review = review_form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            '''
            for 루프를 통해 request.FILES에 전달된 이미지 파일을 순회하면서 ReviewImages 객체를 생성하고 review 객체와 이미지 파일을 연결합니다. 
            '''
            for img in request.FILES.getlist('img'):
                review_image_form = self.get_form(self.second_form_class)
                review_image = review_image_form.save(commit=False)
                review_image.review = review
                review_image.img = img
                review_image.save()
            return self.form_valid(review_form)
        return self.form_invalid(review_form)
    
    '''
    GET 요청을 처리합니다. get_form() 메소드를 사용하여 review_form과 review_image_form을 가져온 후 context에 추가하여 템플릿에 전달합니다.
    '''
    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        review_form = self.get_form(form_class)
        review_image_form = self.get_form(self.second_form_class)
        return self.render_to_response(self.get_context_data(review_form=review_form, review_image_form=review_image_form))

    def form_valid(self, form):
        return super().form_valid(form)
    
    def form_invalid(self, form):
        return super().form_invalid(form)
    

class ReviewDeleteView(LoginRequiredMixin, DeleteView):
    model = Review
    template_name = 'products/product_detail.html'

    def get_success_url(self):
        product_pk = self.kwargs['product_pk']
        return reverse_lazy('products:product_detail', kwargs={'product_pk': product_pk})

    def get_object(self, queryset=None):
        product_pk = self.kwargs['product_pk']
        review_pk = self.kwargs['review_pk']
        review = get_object_or_404(Review, pk=review_pk, product=product_pk)
        return review
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        # 연결된 리뷰 이미지들을 가져와서 삭제합니다.
        review_images = self.object.images.all()
        for review_image in review_images:
            review_image.delete()
        messages.success(request, _('Review has been deleted.'))
        return super().delete(request, *args, **kwargs)


class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = 'products/product_detail.html'
    context_object_name = 'review'
    # success_url = reverse_lazy('products:product_detail')

    #  2. 템플릿에 사용할 수 있는 추가적인 데이터를 컨텍스트에 추가(이미지 폼) -> 리뷰 폼과 리뷰 이미지 수정 폼을 함께 쓸 수 있게 함
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['review_image_form'] = ReviewImageUpdateForm()
        return context

    # 3. 리뷰 수정을 위해 오버라이딩.
    def form_valid(self, form):
        review = form.save(commit=False)
        review.save()
        data = {
            'content': review.content,
            'rating': review.rating,
        }

        # 기존 리뷰 이미지 삭제(변수명은 프론트앤드와 논의해야 함)
        '''
        삭제하고자 하는 이미지에 체크박스를 추가하고, "삭제" 버튼을 누르면 해당 이미지들의 id 값을 existing_images라는 이름의 hidden input에 담아 POST 방식으로 서버에 전송할 수 있습니다.

        또한, 새로운 이미지를 추가하기 위해서는 파일 업로드 필드를 추가하고, "추가" 버튼을 눌렀을 때 파일들을 서버에 업로드하고 새로운 이미지 인스턴스를 생성합니다. 이때도 이미지 파일들을 img라는 이름의 input에 담아 POST 방식으로 서버에 전송합니다.
        '''
        existing_images = self.request.POST.getlist('existing_images')
        ReviewImages.objects.filter(review=review, id__in=existing_images).delete()

        # 새 리뷰 이미지 추가
        review_image_form = ReviewImageUpdateForm(self.request.POST, self.request.FILES)
        if review_image_form.is_valid():
            for img in self.request.FILES.getlist('img'):
                ReviewImages.objects.create(review=review, img=img)

        # 추가된 리뷰 이미지 URL 전달(클라이언트 측에서 AJAX 요청을 통해 리뷰 수정 후 즉시 화면에 새로운 이미지를 보여주기 위해 사용)
        data['image_urls'] = []
        for image in review.images.all():
            data['image_urls'].append(image.img.url)

        return JsonResponse(data)

    # 1. 해당리뷰의 객체를 가져온다.
    def get_object(self, queryset=None):
        review_pk = self.kwargs.get('review_pk')
        return get_object_or_404(Review, pk=review_pk)

    # 4. POST 요청을 처리하기 위해 오버라이딩.
    ## 검증 성공하면 form_valid()메서드 호출하여 리뷰 수정. 
    ## 실패하면 폼 오류 메시지를 화면에 보여줌.
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)

        # 폼 검증
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    

# 후기 조회는 상품 디테일에서 구현됨