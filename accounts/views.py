from django.contrib import messages
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.db.models import F, Sum
from django.db.models.functions import TruncDate
from django.views.generic import FormView, RedirectView, DetailView, UpdateView, DeleteView
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm, CustomUserChangeForm
from products.models import *


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
        context['inquiries'] = inquiries

        review_list = Review.objects.filter(user=self.request.user).prefetch_related('images').order_by('-created_at')
        review_list = review_list.order_by('-created_at')

        context['review_list'] = review_list
        
        purchase_list = Purchase.objects.filter(user=self.request.user)
        purchase_list = purchase_list.order_by('-purchase_date')
        purchase_list = purchase_list.annotate(date=TruncDate('purchase_date'))

        for purchase in purchase_list:
            purchase_items = PurchaseItem.objects.filter(purchase__user=self.request.user, purchase__purchase_date__date=purchase.date)
            purchase.purchase_items = purchase_items

        context['purchase_list'] = purchase_list
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
    success_url = reverse_lazy('index')
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


def permission_denied_view(request, exception):
    return render(request, '403.html', status=403)