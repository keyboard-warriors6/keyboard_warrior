from django.db import transaction
from django.db.models import F, Sum
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.forms import inlineformset_factory, formset_factory
from django.contrib import messages
from django.http import JsonResponse
from django.views.generic import FormView, View, DeleteView
from django.views.generic.edit import CreateView, ProcessFormView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.functions import TruncDate
from products.models import *
from products.forms import *


# 구매하기(Create)
class PurchaseCreateView(LoginRequiredMixin, CreateView):
    model = Purchase
    fields = ['address']
    template_name = 'products/purchase_create.html'
    success_url = reverse_lazy('products:purchase_complete')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_pk = self.request.POST.get('product_pk')
        purchase_items = []
        initial = []
        selected_cart_pks = self.request.POST.getlist('cart_pks')  # 선택된 장바구니 항목의 pk
        if product_pk:
            product = Product.objects.get(pk=product_pk)
            purchase_items.append({'product': product})
            initial.append({'product': product, 'cnt': 1})
        else:
            cart = self.request.session.get('cart', {})
            for product_pk, cnt in cart.items():
                product = Product.objects.get(pk=product_pk)
                purchase_items.append({'product': product, 'cnt': cnt})
                initial.append({'product': product, 'cnt': cnt})
            if selected_cart_pks:  # 선택된 장바구니 항목만 추가
                cart_items = Cart.objects.filter(pk__in=selected_cart_pks)
                for cart_item in cart_items:
                    purchase_items.append({'product': cart_item.product, 'cnt': cart_item.cnt})
                    initial.append({'product': cart_item.product, 'cnt': cart_item.cnt})

        PurchaseItemFormSet = inlineformset_factory(
            Purchase,
            PurchaseItem,
            fields=('product', 'cnt',),
            extra=0,
            can_delete=False,
        )
        formset = PurchaseItemFormSet(initial=initial)
        context['purchase_items'] = purchase_items
        context['formset'] = formset
        print(initial)
        print(formset)
        return context

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        if formset.is_valid():
            self.object = form.save(commit=False)
            self.object.user = self.request.user
            self.object.status = '주문완료'
            self.object.save()
            formset.instance = self.object
            formset.save()
            selected_cart_pks = self.request.GET.getlist('cart_pks')  # 선택된 장바구니 항목의 pk
            if selected_cart_pks:  # 선택된 장바구니 항목 삭제
                cart = self.request.session.get('cart', {})
                for pk in selected_cart_pks:
                    del cart[str(pk)]
                self.request.session['cart'] = cart
            else:
                del self.request.session['cart']  # 장바구니 전체 삭제
            return super().form_valid(form)
        else:
            return self.form_invalid(form)
        
    def form_invalid(self, form):
        self.object = self.model(user=self.request.user, status='주문 실패')
        return super().form_invalid(form)

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return self.handle_no_permission()
        return super().get(request, *args, **kwargs)


class PurchaseCreateFromDetailView(PurchaseCreateView):
    template_name = 'products/product_detail.html'

    def get_initial(self):
        initial = super().get_initial()
        product = get_object_or_404(Product, pk=self.kwargs['pk'])
        initial['product'] = product
        return initial

    def get_success_url(self):
        return reverse('products:purchase_list')    
        
        
        
# # 내가 구매한 상품 목록 조회하기(Read)
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
    

# 장바구니 생성
class CartCreateView(LoginRequiredMixin, FormView):
    form_class = CartForm
    template_name = 'products/product_detail.html'

    def form_valid(self, form):
        product = get_object_or_404(Product, pk=self.kwargs['product_pk'])
        cnt = form.cleaned_data['cnt']
        user = self.request.user
        cart, created = Cart.objects.get_or_create(
            user=user,
            product=product,
            defaults={'cnt': cnt}
        )

        if not created:
            cart.cnt += cnt
            cart.save()

        messages.success(self.request, f'{product.name}이(가) 장바구니에 추가되었습니다.')
        return redirect('products:cart_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = get_object_or_404(Product, pk=self.kwargs['product_pk'])
        context['product'] = product
        context['cart_form'] = CartForm
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = {'cnt': 1}
        return kwargs

    def get_success_url(self):
        return reverse_lazy('products:cart_list')
    

# 장바구니 조회
class CartListView(LoginRequiredMixin, View):
    template_name = 'products/cart_list.html'

    def get(self, request, *args, **kwargs):
        cart_items = Cart.objects.filter(user=request.user)
        total_price = 0

        for item in cart_items:
            item.price = item.cnt * item.product.price
            total_price += item.price

        context = {
            'cart_items': cart_items,
            'total_price': total_price
        }

        return render(request, self.template_name, context)
    

# 장바구니 물건 삭제
class CartDeleteView(LoginRequiredMixin, DeleteView):
    model = Cart
    success_url = reverse_lazy('products:cart_list')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)
    
    def get_object(self, queryset=None):
        cart_pk = self.kwargs.get('cart_pk')
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=cart_pk)
        return obj
    

# 장바구니 물건 수량 수정(비동기)
class CartUpdateView(LoginRequiredMixin, ProcessFormView):
    model = Cart
    fields = ['cnt']

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    def form_valid(self, form):
        self.object = form.save()
        data = {'success': True}
        return JsonResponse(data)

    def form_invalid(self, form):
        data = {'success': False, 'errors': form.errors}
        return JsonResponse(data, status=400)

## 1.    
# class PurchaseCreateView(LoginRequiredMixin, CreateView):
#     model = Purchase
#     form_class = PurchaseForm
#     template_name = 'products/purchase_create.html'
#     success_url = reverse_lazy('products:complete')

#     def get_context_data(self, **kwargs):
#             context = super().get_context_data(**kwargs)
#             user = self.request.user
#             cart_pks = self.request.POST.getlist('cart_item_pks')
#             product_pk = self.request.POST.get('product_pk')

#             if cart_pks:
#             # 선택한 장바구니 항목만 구매하는 경우
#                 cart_items = Cart.objects.filter(user=user, pk__in=cart_pks)
#                 total_price = cart_items.aggregate(total_price=Sum(F('product__price') * F('cnt') * (1 - F('product__discount_rate'))))['total_price']
#                 context['cart_items'] = cart_items
#                 context['total_price'] = total_price
#             elif product_pk:
#                 # 상세 페이지에서 선택한 상품만 구매하는 경우
#                 product = Product.objects.get(pk=product_pk)
#                 total_price = product.price * (1 - product.discount_rate)
#                 context['product'] = product
#                 context['total_price'] = total_price
#             else:
#                 # 전체 장바구니 항목을 구매하는 경우
#                 cart_items = Cart.objects.filter(user=user)
#                 total_price = cart_items.aggregate(total_price=Sum(F('product__price') * F('cnt') * (1 - F('product__discount_rate'))))['total_price']
#                 context['cart_items'] = cart_items
#                 context['total_price'] = total_price

#             return context

#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         kwargs['user'] = self.request.user
#         kwargs['cart_pks'] = self.request.POST.getlist('cart_item_pks')
#         kwargs['product_pk'] = self.request.POST.get('product_pk')
#         return kwargs

#     def form_valid(self, form):
#         response = super().form_valid(form)
#         purchase_items = form.cleaned_data['purchase_items']

#         for purchase_item in purchase_items:
#             purchase_item.purchase = self.object
#             purchase_item.save()

#         # 장바구니에서 선택한 상품이 있다면, 해당 상품들은 구매 완료 후 삭제
#         cart_pks = self.request.POST.getlist('cart_item_ids')
#         if cart_pks:
#             Cart.objects.filter(user=self.request.user, pk__in=cart_pks).delete()

#         return response

#     def get_success_url(self):
#         messages.success(self.request, '구매가 완료되었습니다.')
#         return super().get_success_url()


## 2.
# class PurchaseCreateView(LoginRequiredMixin, CreateView):
#     model = Purchase
#     form_class = PurchaseForm
#     template_name = 'products/purchase_create.html'
#     success_url = reverse_lazy('products:complete')
#     PurchaseItemFormSet = inlineformset_factory(
#         Purchase,
#         PurchaseItem,
#         fields=('cnt', 'product'),
#         extra=0,
#         can_delete=False,
#     )

#     def get_initial(self):
#         initial = super().get_initial()
#         cart_pk = self.request.GET.get('cart_pk')
#         product_pk = self.request.GET.get('product_pk')
#         cnt = self.request.GET.get('cnt')
#         if cart_pk:
#             cart_item = Cart.objects.get(pk=cart_pk, user=self.request.user)
#             initial['product'] = cart_item.product
#             initial['cnt'] = cart_item.cnt
#             initial['purchase_items'] = [
#                 {
#                     'product': cart_item.product,
#                     'cnt': cart_item.cnt,
#                 }
#             ]
#         elif product_pk and cnt:
#             product = Product.objects.get(pk=product_pk)
#             initial['product'] = product
#             initial['cnt'] = cnt
#             initial['purchase_items'] = [
#                 {
#                     'product': product,
#                     'cnt': cnt,
#                 }
#             ]
#         return initial
    
#     def get_form_kwargs(self):
#         kwargs = super().get_form_kwargs()
#         kwargs['user'] = self.request.user
#         return kwargs
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         if self.request.method == 'POST':
#             context['purchase_item_formset'] = self.PurchaseItemFormSet(
#                 self.request.POST,
#                 instance=self.object,
#             )
#         else:
#             initial = self.get_initial()
#             context['purchase_item_formset'] = self.PurchaseItemFormSet(
#                 instance=self.object,
#                 initial=initial['purchase_items'],
#             )
#         context['total_price'] = self.object.total_price if self.object else 0
#         return context
    
#     def create(self, form):
#         self.object = form.save(commit=False)
#         self.object.user = self.request.user
#         self.object.status = '주문 완료'
#         self.object.save()
#         return self.object
    
#     def form_invalid(self, form):
#         self.object = self.model(user=self.request.user, status='주문 실패')
#         return super().form_invalid(form)
    
#     def form_valid(self, form):
#         context = self.get_context_data()
#         purchase_item_formset = context['purchase_item_formset']
#         if purchase_item_formset.is_valid():
#             self.create(form)
#             purchase_item_formset.instance = self.object
#             purchase_item_formset.save()
#             Cart.objects.filter(user=self.request.user).delete()
#             return super().form_valid(form)
#         else:
#             return self.form_invalid(form)