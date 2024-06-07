from rest_framework import serializers

from order.models import Order, OrderItem
from product.models import Image


class OrderItemSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source='product.title')
    product_price = serializers.IntegerField(source='product.price')
    main_image = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = ['product_title', 'product_price', 'main_image', 'quantity', 'total_price']

    def get_main_image(self, obj):
        main_image = Image.objects.filter(product=obj.product).first()
        if main_image:
            return main_image.image.url
        return ""


class OrderSerializer(serializers.ModelSerializer):
    order_items = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['pk', 'total_price', 'order_items']

    def get_order_items(self, obj):
        order_items = OrderItem.objects.filter(order=obj)
        serializer = OrderItemSerializer(order_items, many=True)
        return serializer.data
