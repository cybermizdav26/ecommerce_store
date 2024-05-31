from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView

from account.api.version1.serializers import UserSerializer

User = get_user_model()


class SignUp(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
