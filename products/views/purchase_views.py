from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.forms import inlineformset_factory
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from products.models import *
from products.forms import *

class PurchaseCreateView(CreateView):
    model = Purchase
    form_class = PurchaseForm
    template_name = 'products/create.html'
    success_url = reverse_lazy('products:complete')

    '''
    inlineformset_factory 함수를 사용해 동적으로 생성된 폼셋 클래스입니다. 이 폼셋 클래스는 Purchase 모델과 PurchaseItem 모델 간의 관계를 나타냅니다. fields 매개변수에는 폼셋에 포함될 필드 목록을 지정합니다. extra 매개변수는 초기 폼셋에 몇 개의 빈 폼이 포함될지 지정합니다. can_delete 매개변수는 사용자가 폼셋에서 항목을 삭제할 수 있는지 여부를 지정합니다.
    '''
    CartFormSet = inlineformset_factory(
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
        product_id = self.request.GET.get('product_id')
        cnt = self.request.GET.get('cnt')
        if product_id:
            product = get_object_or_404(Product, pk=product_id)
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
            context['cart_formset'] = self.CartFormSet(
                self.request.POST,
                instance=self.object,
            )
        else:
            initial = self.get_initial()
            context['cart_formset'] = self.CartFormSet(
                instance=self.object,
                initial=initial['purchase_items'],
            )
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        cart_formset = context['cart_formset']
        if cart_formset.is_valid():
            self.object = form.save(commit=False)
            self.object.user = self.request.user
            self.object.status = Purchase.STATUS_ORDERED
            self.object.save()
            cart_formset.instance = self.object
            cart_formset.save()
            Cart.objects.filter(user=self.request.user).delete()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)