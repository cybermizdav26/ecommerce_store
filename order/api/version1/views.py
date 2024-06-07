from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from order.api.version1.serializers import OrderSerializer
from order.models import Order, OrderItem
from product.models import Product


class CartByOwnerListAPIView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(customer=self.request.user, ordered=False)
        return qs


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_order(request, pk):
    product = get_object_or_404(Product, pk=pk)
    order, order_created = Order.objects.get_or_create(
        customer=request.user,
        ordered=False
    )

    try:
        order_item, order_item_created = OrderItem.objects.get_or_create(
            product=product,
            customer=request.user,
            ordered=False,
            order=order

        )
    except IntegrityError:
        order_item, order_item_created = OrderItem.objects.get_or_create(
            product=product,
            customer=request.user,
            quantity=1,
            ordered=False,
            order=order

        )
    order_item.set_total_price()
    if not order_item_created:
        order_item.quantity += 1
        order_item.save()
        order_item.set_total_price()
        return Response({'message': "updated to 1"}, status=status.HTTP_201_CREATED)
    return Response({'message': "order created"}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reduce_order(request, pk):
    order = Order.objects.filter(customer=request.user, ordered=False).first()

    if not order:
        return Response({"message": "You do not have an active order"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        order_item = get_object_or_404(OrderItem, pk=pk)
    except OrderItem.DoesNotExist:
        return Response({'message': "This item is not in your cart"}, status=status.HTTP_400_BAD_REQUEST)

    if order_item.quantity > 1:
        order_item.quantity -= 1
        order_item.set_total_price()
    else:
        order_item.delete()

    return Response({"message": "Item quantity was updated"}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def remove_order_item(request, pk):
    order_item = get_object_or_404(OrderItem, pk=pk)
    order_item.delete()
    return Response({"message": "Item deleted successfully"}, status=status.HTTP_200_OK)
