from django.db import transaction
from django.db.models import F, Sum
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.forms import inlineformset_factory, formset_factory
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.views.generic import FormView, View, DeleteView
from django.views.generic.edit import CreateView, FormMixin, UpdateView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models.functions import TruncDate
from products.models import *
from products.forms import *


# 구매하기(Create)
class PurchaseFromCartView(LoginRequiredMixin, CreateView):
    model = Purchase
    fields = ['address']
    template_name = 'products/purchase_create.html'
    success_url = reverse_lazy('products:product_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        purchase_items = []
        selected_cart_pks = self.request.POST.getlist('cart_pks')  # 
        cart = Cart.objects.all()
        if len(selected_cart_pks) != len(cart):  # 선택된 장바구니 항목만 추가
            cart_items = Cart.objects.filter(pk__in=selected_cart_pks)
            for cart_item in cart_items:
                purchase_items.append({'product': cart_item.product, 'cnt': cart_item.cnt})
        else:
            cart_items = cart
            for cart_item in cart_items:
                purchase_items.append({'product': cart_item.product, 'cnt': cart_item.cnt})
        context['purchase_items'] = purchase_items
        cart_pks = []
        for pk in selected_cart_pks:
            cart_pks.append(int(pk))
        context['cart_pks'] = cart_pks

        return context


    def delete_cart_items(self, cart_items):
        for cart_item in cart_items:
            cart_item.delete()

    def form_valid(self, form):
        cnts = self.request.POST.getlist('cnts')
        products_1 = self.request.POST.getlist('products_1')
        products = []
        for product_pk in products_1:
            product = Product.objects.get(pk=product_pk)
            products.append(product)

        selected_cart_pks = self.request.POST.get('cart_pks').strip('[]')
        selected_cart_pks = list(map(int, selected_cart_pks.split(',')))

        purchase_items = []
        for i in range(len(cnts)):
            purchase_items.append({'product': products[i], 'cnt': cnts[i]})

        cart = Cart.objects.all()
        
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.status = '주문완료'
        self.object.save()

        for item in purchase_items:
            purchase_item = PurchaseItem()
            purchase_item.purchase = self.object
            purchase_item.product = item['product']
            purchase_item.cnt = item['cnt']
            purchase_item.save()

        if len(selected_cart_pks) != len(cart):  # 선택된 장바구니 항목만 삭제
            cart_items = Cart.objects.filter(pk__in=selected_cart_pks)
            self.delete_cart_items(cart_items)
        else:  # 전체 삭제
            cart_items = cart
            self.delete_cart_items(cart_items)
        return super().form_valid(form)
        
    def form_invalid(self, form):
        self.object = self.model(user=self.request.user, status='주문 실패')
        return super().form_invalid(form)

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return self.handle_no_permission()
        return super().get(request, *args, **kwargs)


class PurchaseFromDetailView(LoginRequiredMixin, CreateView):
    template_name = 'products/purchase_detail.html'
    model = Purchase
    fields = ['address']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = get_object_or_404(Product, pk=self.kwargs['product_pk'])
        context['product'] = product
        context['cnt'] = self.request.POST.get('cnt', 1)
        return context
    
    def form_valid(self, form):
        product = get_object_or_404(Product, pk=self.kwargs['product_pk'])
        cnt = self.request.POST.get('cnt')
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.status = '주문완료'
        self.object.save()

        purchase_item = PurchaseItem()
        purchase_item.product = product
        purchase_item.purchase = self.object
        purchase_item.cnt = cnt
        purchase_item.save()

        return redirect('products:product_list')

        
        
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
class CartDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Cart
    success_url = reverse_lazy('products:cart_list')

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)
    
    def get_object(self, queryset=None):
        if 'delete_all' in self.request.POST:
            queryset = self.get_queryset()
            obj = queryset.first()  # 첫 번째 Cart 객체를 가져옴
            return obj
        else:
            cart_pk = self.kwargs.get('cart_pk')
            queryset = self.get_queryset()
            obj = get_object_or_404(queryset, pk=cart_pk)
            return obj
        
    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user    
    
    def delete(self, request, *args, **kwargs):
        if 'delete_all' in request.POST:
            self.get_queryset().delete()
        else:
            cart_pk = kwargs.get('cart_pk')
            queryset = self.get_queryset()
            obj = get_object_or_404(queryset, pk=cart_pk)
            obj.delete()
        return HttpResponseRedirect(self.success_url)
        

# 장바구니 물건 수량 수정(비동기)
class CartUpdateView(LoginRequiredMixin, UpdateView, FormMixin):
    model = Cart
    fields = ['cnt']

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            self.object.cnt = form.cleaned_data['cnt']
            self.object.save()

            data = {'success': True}
            return JsonResponse(data)
        else:
            data = {'success': False, 'errors': form.errors}
            return JsonResponse(data, status=400)