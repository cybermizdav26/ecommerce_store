from rest_framework import generics

from product.api.version1.serializer import CategorySerializer, ProductsSerializer, ProductDetailSerializer
from product.models import Category, Product


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    # def get_queryset(self):
    #     qs = super().get_queryset()
    #     id = [1, 3]
    #     qs = qs.filter(id__in=id)
    #     return qs


class ProductsListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductsSerializer


class ProductsByCategoryListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductsSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        pk = self.kwargs.get('pk')
        qs = qs.filter(category=pk)
        return qs


class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer
