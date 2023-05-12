from django.urls import path
from .views import *

app_name = 'products'
urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('create/', ProductCreateView.as_view(), name='product_create'),
    path('<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),

    # 후기
    path('product/<int:pk>/review/', ReviewCreateView.as_view(), name='review_create'),
    path('product/<int:pk>/review/<int:review_pk>/delete/', ReviewDeleteView.as_view(), name='review_delete'),
    path('products/<int:pk>/review/<int:review_pk>/update/', ReviewUpdateView.as_view(), name='review_update'),
]