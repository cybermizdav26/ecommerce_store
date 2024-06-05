from django.urls import path

from product.api.version1.views import (CategoryListAPIView, ProductsListAPIView, ProductDetailAPIView,
                                        CategoryCreateAPIView, CommentCreateAPIView)

urlpatterns = [
    path('category-create/', CategoryCreateAPIView.as_view(), name='category-create'),
    path('categories/', CategoryListAPIView.as_view(), name='categories'),
    path('category/<int:pk>', ProductsListAPIView.as_view(), name='category'),
    path('products/', ProductsListAPIView.as_view(), name='products'),
    path('product/<int:pk>', ProductDetailAPIView.as_view(), name='product'),
    path('comment-create/', CommentCreateAPIView.as_view(), name='comment-create')
]