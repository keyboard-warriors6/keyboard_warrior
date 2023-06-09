from django.contrib import messages
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from django.db.models import F, Sum, Count
from django.db.models.functions import TruncDate
from django.views.generic import FormView, RedirectView, DetailView, UpdateView, DeleteView
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm, CustomUserChangeForm
from products.models import *
from itertools import groupby
from operator import itemgetter
from django.utils import timezone
from datetime import timedelta

class SignupView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'accounts/signup.html'


class LoginView(FormView):
    form_class = AuthenticationForm
    success_url = reverse_lazy('products:product_list')
    template_name = 'accounts/login.html'


    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)
    

class LogoutView(RedirectView):
    url = reverse_lazy('products:product_list')

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)
    
    
class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = 'accounts/profile.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object
        
        inquiries = user.inquiry_set.filter(user=self.request.user)
        sort_param = self.request.GET.get('sort')

        # if sort_param == 'answer':
        #     for inquiry in inquiries:
        #         if inquiry.answer:
        #             inquiries = inquiries.order_by('-created_at')
                    
        if sort_param == 'answer':
            inquiries = inquiries.filter(answer__isnull=False)
        elif sort_param == 'all':
            pass

        context['inquiries'] = inquiries

        review_list = Review.objects.filter(user=self.request.user).prefetch_related('images')
        sort_param = self.request.GET.get('sort')
        
        if sort_param == 'rating':
            review_list = review_list.order_by('-rating', '-created_at')
            
        elif sort_param == 'created_at':
            review_list = review_list.order_by('-created_at', '-rating')
        
        context['review_list'] = review_list

        # 주문 현황 가져오기
        purchases = Purchase.objects.filter(user=user).annotate(item_count=Count('products')).order_by('-purchase_date')

        if sort_param == '1hour':
            time_range = timedelta(hours=1)
            purchases = purchases.filter(purchase_date__gte=timezone.now() - time_range)
        elif sort_param == '12hours':
            time_range = timedelta(hours=12)
            purchases = purchases.filter(purchase_date__gte=timezone.now() - time_range)
        else:
            time_range = None

    
        # 날짜와 시간을 구분하여 묶어주기
        grouped_purchases = []
        for purchase in purchases:
            grouped_purchases.append((purchase.purchase_date.date(), purchase))

        grouped_purchases.sort(key=itemgetter(0), reverse=True)
        grouped_purchases_by_date = {
            date: [purchase for _, purchase in group]
            for date, group in groupby(grouped_purchases, key=itemgetter(0))
        }
        context['purchases'] = grouped_purchases_by_date

        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = CustomUserChangeForm
    template_name = 'accounts/update.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'


    def get_success_url(self):
        return reverse_lazy('accounts:profile', kwargs={'username': self.request.user.username})


    def get_object(self, queryset=None):
        return self.request.user


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = get_user_model()
    success_url = reverse_lazy('products:product_list')
    slug_field = 'username'
    slug_url_kwarg = 'username'


    def get_object(self, queryset=None):
        return self.request.user


    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        messages.success(request, _('Your account has been deleted.'))
        request.session.flush()
        return redirect(self.success_url)

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

def permission_denied_view(request, exception):
    return render(request, '403.html', status=403)

#         context['purchase_items_by_date'] = purchase_items_by_date

#         return context
    