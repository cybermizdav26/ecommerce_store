from django.contrib import admin

from order.models import Order, OrderItem

admin.site.register(OrderItem)
admin.site.register(Order)
