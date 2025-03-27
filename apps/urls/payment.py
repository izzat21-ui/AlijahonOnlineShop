from apps.views import ThreadRequest, PaymentTemplateView
from django.urls import path

urlpatterns = [
    path("payment", PaymentTemplateView.as_view(), name='payment'),
]
