from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView, UpdateAPIView

from account.api.version1.serializers import UserCreateSerializer, UserUpdateSerializer

User = get_user_model()


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class UserUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
