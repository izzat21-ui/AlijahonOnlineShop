from apps.views import  PaymentFormView
from django.urls import path

urlpatterns = [
    path("payment", PaymentFormView.as_view(), name='payment'),
]
