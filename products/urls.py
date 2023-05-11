from django.urls import path
from . import views

app_name = 'products'
urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),


    # 후기
    path('product/<int:pk>/review/', views.ReviewCreateView.as_view(), name='review_create'),
    path('product/<int:pk>/review/<int:review_pk>/delete/', views.ReviewDeleteView.as_view(), name='review_delete'),
    path('products/<int:pk>/review/<int:review_pk>/update/', views.ReviewUpdateView.as_view(), name='review_update'),

]