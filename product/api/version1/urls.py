from django.urls import path

from product.api.version1.views import CategoryListAPIView, ProductsListAPIView, ProductDetailAPIView

urlpatterns = [
    path('categories/', CategoryListAPIView.as_view(), name='categories'),
    path('products/', ProductsListAPIView.as_view(), name='products'),
    path('category/<int:pk>', ProductsListAPIView.as_view(), name='category'),
    path('product/<int:pk>', ProductDetailAPIView.as_view(), name='product'),
]