from django.db import models


class UserType(models.IntegerChoices):
    ADMINISTRATOR = 0, 'Admin'
    CUSTOMER = 1, 'Customer'
