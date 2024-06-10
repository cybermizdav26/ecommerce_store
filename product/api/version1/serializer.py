from rest_framework import serializers

from product.models import Category, Product, Image, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['pk', 'name', 'order', 'type']


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']


class ProductSerializer(serializers.ModelSerializer):
    main_image = serializers.CharField()

    class Meta:
        model = Product
        fields = ['pk', 'title', 'description', 'price', 'main_image']

    def get_main_image(self, obj):
        main_image = obj.image_set.first()
        if main_image:
            return main_image.image.url
        return ""


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['image']


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['owner', 'text', 'star']


class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    images = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['pk', 'title', 'description', 'price', 'quantity', 'images', 'category', 'detail', 'comments']

    def get_images(self, obj):
        images = Image.objects.filter(product=obj)
        serializer = ImageSerializer(images, many=True)
        return serializer.data

    def get_comments(self, obj):
        comments = Comment.objects.filter(product=obj)
        serializer = CommentSerializer(comments, many=True)
        return serializer.data


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['text', 'star', 'product']


