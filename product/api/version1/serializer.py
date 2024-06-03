from rest_framework import serializers

from product.models import Category, Product, Image


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['pk', 'name', 'order', 'type']


class ProductsSerializer(serializers.ModelSerializer):
    main_image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['pk', 'title', 'description', 'price', 'main_image']

    def get_main_image(self, obj):
        main_image = Image.objects.filter(product=obj).first()
        if main_image:
            return main_image.image.url
        return ""


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['image']


class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['pk', 'title', 'description', 'price', 'quantity', 'images', 'category', 'detail']

    def get_images(self, obj):
        images = Image.objects.filter(product=obj)
        serializer = ImageSerializer(images, many=True)
        return serializer.data
