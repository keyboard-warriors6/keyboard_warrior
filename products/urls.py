from django.urls import path
from .views import *

app_name = 'products'
urlpatterns = [
    # 상품
    path('', ProductListView.as_view(), name='product_list'),
    path('create/', ProductCreateView.as_view(), name='product_create'),
    path('search/', ProductSearchView.as_view(), name='product_search'),
    path('category/', ProductCategoryView.as_view(), name='product_category'),
    path('<int:product_pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('<int:product_pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    path('<int:product_pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('<int:product_pk>/bookmark/', ProductBookmarkView.as_view(), name='product_bookmark'),
    path('keyboard_trend/', KeyboardTrendView.as_view(), name='keyboard_trend'),
    path('my_bookmark/', BookmarkedProductListView.as_view(), name='bookmarked_products'),
    
    # 후기
    path('<int:product_pk>/review/', ReviewCreateView.as_view(), name='review_create'),
    path('<int:product_pk>/review/<int:review_pk>/delete/', ReviewDeleteView.as_view(), name='review_delete'),
    path('<int:product_pk>/review/<int:review_pk>/update/', ReviewUpdateView.as_view(), name='review_update'),
    path('review/<int:review_pk>/likes/', ReviewLikeView.as_view(), name='review_like'),


    # 구매
    ## 다중 구매(from 장바구니)
    path('purchase_create/', PurchaseFromCartView.as_view(), name='purchase_from_cart'),
    ## 상세페이지 구매
    path('<int:product_pk>/purchase/', PurchaseFromDetailView.as_view(), name='purchase_from_detail'),
    ## 구매완료
    path('purchase_complete/<int:purchase_pk>/', PurchaseCompleteView.as_view(), name='purchase_complete'),

    # 장바구니
    path('cart/', CartListView.as_view(), name='cart_list'),
    path('<int:product_pk>/add-to-cart/', CartCreateView.as_view(), name='cart_create'),
    path('cart/<int:cart_pk>/delete/', CartDeleteView.as_view(), name='cart_delete'),
    path('cart/<int:cart_pk>/update/', CartUpdateView.as_view(), name='cart_update'),

    # 문의, 답변
    path('<int:product_pk>/inquiry/create/', InquiryCreateView.as_view(), name='inquiry_create'),
    path('<int:product_pk>/inquiry/<int:inquiry_pk>/update/', InquiryUpdateView.as_view(), name='inquiry_update'),
    path('<int:product_pk>/inquiry/<int:inquiry_pk>/delete/', InquiryDeleteView.as_view(), name='inquiry_delete'),
    path('<int:product_pk>/inquiry/<int:inquiry_pk>/create/', AnswerCreateView.as_view(), name='answer_create'),
    path('<int:product_pk>/inquiry/<int:inquiry_pk>/<int:answer_pk>/update/', AnswerUpdateView.as_view(), name='answer_update'),
    path('<int:product_pk>/inquiry/<int:inquiry_pk>/<int:answer_pk>/delete/', AnswerDeleteView.as_view(), name='answer_delete'),
]