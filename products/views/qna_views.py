from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView
from products.forms import *
from products.models import *


class InquiryCreateView(CreateView):
    model = Inquiry
    form_class = InquiryForm
    template_name = 'products/inquiry_create.html'


    def form_valid(self, form):
        product = Product.objects.get(pk=self.kwargs['pk'])
        form.instance.product = product
        form.instance.user = self.request.user
        return super().form_valid(form)


    def get_success_url(self):
        return reverse_lazy('products:product_detail', kwargs={'pk': self.kwargs['pk']})


class InquiryUpdateView(UpdateView):
    model = Inquiry
    form_class = InquiryForm
    template_name = 'products/inquiry_update.html'


    def get_object(self, queryset=None):
        product_pk = self.kwargs.get('pk')
        inquiry_pk = self.kwargs.get('inquiry_pk')
        return Inquiry.objects.get(pk=inquiry_pk, product__pk=product_pk)


    def get_success_url(self):
        product_pk = self.kwargs.get('pk')
        return reverse_lazy('products:product_detail', args=[product_pk])


class InquiryDeleteView(DeleteView):
    model = Inquiry


    def get_object(self, queryset=None):
        product_pk = self.kwargs.get('pk')
        inquiry_pk = self.kwargs.get('inquiry_pk')
        return Inquiry.objects.get(pk=inquiry_pk, product__pk=product_pk)


    def get_success_url(self):
        product_pk = self.kwargs.get('pk')
        return reverse_lazy('products:product_detail', args=[product_pk])


    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


class AnswerCreateView(CreateView):
    model = Answer
    form_class = AnswerForm
    template_name = 'products/answer_create.html'


    def form_valid(self, form):
        inquiry = Inquiry.objects.get(pk=self.kwargs['inquiry_pk'])
        form.instance.inquiry = inquiry
        return super().form_valid(form)


    def get_success_url(self):
        return reverse_lazy('products:product_detail', kwargs={'pk': self.kwargs['pk']})


class AnswerUpdateView(UpdateView):
    model = Answer
    form_class = AnswerForm
    template_name = 'products/inquiry_update.html'


    def get_object(self, queryset=None):
        inquiry_pk = self.kwargs.get('inquiry_pk')
        answer_pk = self.kwargs.get('answer_pk')
        return Answer.objects.get(pk=answer_pk, inquiry__pk=inquiry_pk)
    

    def get_success_url(self):
        product_pk = self.kwargs.get('pk')
        return reverse_lazy('products:product_detail', args=[product_pk])


class AnswerDeleteView(DeleteView):
    model = Answer

    
    def get_object(self, queryset=None):
        inquiry_pk = self.kwargs.get('inquiry_pk')
        answer_pk = self.kwargs.get('answer_pk')
        return Answer.objects.get(pk=answer_pk, inquiry__pk=inquiry_pk)


    def get_success_url(self):
        product_pk = self.kwargs.get('pk')
        return reverse_lazy('products:product_detail', args=[product_pk])


    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)