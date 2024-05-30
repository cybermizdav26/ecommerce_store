from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Sum
from django.shortcuts import redirect, get_object_or_404

from order.models import Order, OrderItem
from product import views
from product.models import Product


@login_required(login_url='accounts/login')
def cart(request):
    order = Order.objects.filter(customer=request.user, ordered=False).annotate(
        order_tota_price=Sum('orderitem__total_price')
    ).first()
    context = {"order": order}
    return redirect(request, 'order/carts.html', context=context)


@login_required(login_url='accounts/login')
def add_order(request, pk):
    product = get_object_or_404(Product, pk=pk)
    order, order_created = Order.objects.get_or_create(
        customer=request.user,
        ordered=False
    )

    try:
        order_item, order_item_created = Order.objects.get_or_create(
            product=product,
            customer=request.user,
            ordered=False,
            order=order,
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
