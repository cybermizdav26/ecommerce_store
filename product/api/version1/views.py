from django.core.cache import cache
from django.db.models import OuterRef, Subquery
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from product.api.version1.serializer import (
    CategorySerializer, ProductDetailSerializer,
    CategoryCreateSerializer, CommentCreateSerializer, ProductSerializer
)
from product.models import Category, Product, Comment, Image


class CategoryCreateAPIView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryCreateSerializer


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
    serializer_class = ProductSerializer

    def get_queryset(self):
        products = cache.get('product_list')
        if products is None:
            # products = Product.objects.prefetch_related(
            #     Prefetch('image_set', queryset=Image.objects.order_by('id'))
            # )
            main_image_subquery = Image.objects.filter(
                product=OuterRef('pk'),
                # is_main=True
            ).values('image')[:1]

            products = Product.objects.annotate(
                main_image=Subquery(main_image_subquery)
            )

            cache.set('product_list', products)
        # cache.delete('product_list')
        return products


class ProductsByCategoryListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        pk = self.kwargs.get('pk')
        qs = qs.filter(category=pk)
        return qs


class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer


class CommentCreateAPIView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer
    permission_classes = (IsAuthenticated, )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
