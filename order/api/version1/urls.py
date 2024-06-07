from django.urls import path

from order.api.version1.views import CartByOwnerListAPIView, add_order, reduce_order, remove_order_item


urlpatterns = [
    path('cart/', CartByOwnerListAPIView.as_view(), name='cart'),
    path('add/<int:pk>/', add_order, name='add'),
    path('reduce/<int:pk>/', reduce_order, name='reduce'),
    path('remove/<int:pk>/', remove_order_item, name='remove')
]