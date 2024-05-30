from django.db import models


class CategoryType(models.IntegerChoices):
    NON_TYPE = 0, 'Non-type'
    CLOTHES = 1, 'Clothes',
    FOODS = 2, 'Food'
    BOOKS = 3, 'Books',
    ELECTRONICS = 4, 'Electronics',
    ACCESSORIES = 5, 'Accessories'
