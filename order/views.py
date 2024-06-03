from django.contrib.auth.decorators import login_required
from django.db.models import F, Sum
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db import IntegrityError

from order.models import Order, OrderItem
from product.models import Product


@login_required(login_url='/account/login/')
def cart(request):
    order = Order.objects.filter(customer=request.user,
                                 ordered=False).annotate(
        order_total_price=Sum('order_items__total_price')
    ).first()

    context = {
        'order': order
    }
    return render(request, 'order/cart.html', context=context)


@login_required(login_url='/account/login/')
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
        messages.info(request, f'{product.title} updated to 1!')
        return redirect('order:cart')
    messages.info(request, 'Added to cart!')
    return redirect('order:cart')


@login_required(login_url='/account/login/')
def remove_order_item(request, pk):
    order_item = get_object_or_404(OrderItem, pk=pk)
    order_item.delete()
    return redirect('order:cart')


@login_required(login_url='/account/login')
def reduce_order(request, pk):
    order = Order.objects.filter(customer=request.user, ordered=False).first()

    if not order:
        messages.info(request, "You do not have an active order")
        return redirect("order:cart")

    try:
        order_item = get_object_or_404(OrderItem, pk=pk)
    except OrderItem.DoesNotExist:
        messages.info(request, "This item is not in your cart")
        return redirect("order:cart")

    if order_item.quantity > 1:
        order_item.quantity -= 1
        order_item.set_total_price()
    else:
        order_item.delete()

    messages.info(request, "Item quantity was updated")
    return redirect("order:cart")
