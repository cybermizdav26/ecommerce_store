from django.contrib.auth.models import AbstractUser
from django.db import models

from account.choises import UserType


class User(AbstractUser):
    user_type = models.IntegerField(choices=UserType.choices, default=UserType.CUSTOMER)
    phone = models.CharField(max_length=13, null=True, blank=True)
    image = models.ImageField(upload_to='user_photos/', null=False, blank=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.user_type == 0

    @property
    def is_customer(self):
        return self.user_type == 1

