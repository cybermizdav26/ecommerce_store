from django.contrib import admin

from .models import Category, Product, Image, Comment

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Image)
admin.site.register(Comment)