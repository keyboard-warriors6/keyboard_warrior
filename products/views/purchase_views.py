from typing import Any
from django.db.models import F, Sum
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.forms import inlineformset_factory
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.functions import TruncDate
from products.models import *
from products.forms import *



# 구매하기(Create)
class PurchaseCreateView(LoginRequiredMixin, CreateView):
    model = Purchase
    form_class = PurchaseForm
    template_name = 'products/create.html'
    success_url = reverse_lazy('products:complete')

    '''
    inlineformset_factory 함수를 사용해 동적으로 생성된 폼셋 클래스입니다. 이 폼셋 클래스는 Purchase 모델과 PurchaseItem 모델 간의 관계를 나타냅니다. fields 매개변수에는 폼셋에 포함될 필드 목록을 지정합니다. extra 매개변수는 초기 폼셋에 몇 개의 빈 폼이 포함될지 지정합니다. can_delete 매개변수는 사용자가 폼셋에서 항목을 삭제할 수 있는지 여부를 지정합니다.
    '''
    PurchaseItemFormSet = inlineformset_factory(
        Purchase,
        PurchaseItem,
        fields=('cnt', 'product'),
        extra=0,
        can_delete=False,
    )

    '''
    get_form_kwargs(self): 폼 인스턴스를 만들 때 사용할 인수를 반환하는 메서드. user 인수를 추가하여 폼이 사용자 정보를 알 수 있도록 함.
    '''
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    '''
    폼 인스턴스를 만들 때 초기값을 설정하는 메서드입니다. 상세 페이지에서 구매 버튼을 눌렀을 때는 해당 상품과 수량을 폼에 미리 채워 넣습니다. 장바구니에서 구매 버튼을 눌렀을 때는 장바구니에 담긴 모든 항목의 정보를 폼에 미리 채워 넣습니다.
    '''

    def get_initial(self):
        initial = super().get_initial()
        product_id = self.request.GET.get('pk')
        cnt = self.request.GET.get('cnt')
        if product_id:
            product = get_object_or_404(Product, pk=product_id)
            cnt = cnt if cnt and cnt.isdigit() else 1
            initial['purchase_items'] = [{'product': product, 'cnt': cnt}]
        else:
            initial['purchase_items'] = [
                {'product': item.product, 'cnt': item.cnt}
                for item in Cart.objects.filter(user=self.request.user)
            ]
        return initial
    
    '''
    템플릿에서 사용할 컨텍스트 데이터를 반환하는 메서드입니다. POST 요청인 경우 폼셋을 바인딩합니다. GET 요청인 경우 폼셋에 초기값을 설정합니다.
    '''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == 'POST':
            context['purchase_item_formset'] = self.PurchaseItemFormSet(
                self.request.POST,
                instance=self.object,
            )
        else:
            initial = self.get_initial()
            context['purchase_item_formset'] = self.PurchaseItemFormSet(
                instance=self.object,
                initial=initial['purchase_items'],
            )
        context['total_price'] = self.object.total_price
        return context
    
    def form_invalid(self, form):
        self.object = self.model(user=self.request.user, status='주문 실패')
        return super().form_invalid(form)
    
    def form_valid(self, form):
        context = self.get_context_data()
        purchase_item_formset = context['purchase_item_formset']
        if purchase_item_formset.is_valid():
            self.object = form.save(commit=False)
            self.object.user = self.request.user
            self.object.status = '주문 완료'
            self.object.save()
            purchase_item_formset.instance = self.object
            purchase_item_formset.save()
            Cart.objects.filter(user=self.request.user).delete()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)
        
        
# 내가 구매한 상품 목록 조회하기(Read)
class PurchaseListView(LoginRequiredMixin, ListView):
    model = Purchase
    template_name = 'products:purchase_list.html'
    context_object_name = 'purchase_list'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(user=self.request.user)
        queryset = queryset.order_by('-purchase_date')
        queryset = queryset.annotate(date=TruncDate('purchase_date'))
        queryset = queryset.values('date').annotate(total_price=Sum(F('purchaseitem__product__price') * F('purchaseitem__cnt')))

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for purchase in context['purchase_list']:
            purchase_items = purchase.purchaseitem_set.all()
            purchase.purchase_items = purchase_items

        return context