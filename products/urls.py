from django.urls import path
from .views import *

app_name = 'products'
urlpatterns = [
    # 상품
    path('', ProductListView.as_view(), name='product_list'),
    path('create/', ProductCreateView.as_view(), name='product_create'),
    path('<int:product_pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('<int:product_pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('<int:product_pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
  
    # 후기
    path('<int:product_pk>/review/', ReviewCreateView.as_view(), name='review_create'),
    path('<int:product_pk>/review/<int:review_pk>/delete/', ReviewDeleteView.as_view(), name='review_delete'),
    path('<int:product_pk>/review/<int:review_pk>/update/', ReviewUpdateView.as_view(), name='review_update'),
  
    # 구매
    path('purchase_create/', PurchaseCreateView.as_view(), name='purchase_create'),
    path('purchase_list/', PurchaseListView.as_view(), name='purchase_list'),

    # 문의, 답변
    path('<int:product_pk>/inquiry/create/', InquiryCreateView.as_view(), name='inquiry_create'),
    path('<int:product_pk>/inquiry/<int:inquiry_pk>/update/', InquiryUpdateView.as_view(), name='inquiry_update'),
    path('<int:product_pk>/inquiry/<int:inquiry_pk>/delete/', InquiryDeleteView.as_view(), name='inquiry_delete'),
    path('<int:product_pk>/inquiry/<int:inquiry_pk>/create/', AnswerCreateView.as_view(), name='answer_create'),
    path('<int:product_pk>/inquiry/<int:inquiry_pk>/<int:answer_pk>/update/', AnswerUpdateView.as_view(), name='answer_update'),
    path('<int:product_pk>/inquiry/<int:inquiry_pk>/<int:answer_pk>/delete/', AnswerDeleteView.as_view(), name='answer_delete'),
]