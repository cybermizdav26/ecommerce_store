from django.urls import path

from account.api.version1.views import SignUp

urlpatterns = [
    path('create', SignUp.as_view(), name='create')
]