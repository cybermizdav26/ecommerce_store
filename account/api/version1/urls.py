from django.urls import path

from account.api.version1.views import UserCreateAPIView, UserUpdateAPIView

urlpatterns = [
    path('create/', UserCreateAPIView.as_view(), name='create'),
    path('update/<int:pk>', UserUpdateAPIView.as_view(), name='update'),
]