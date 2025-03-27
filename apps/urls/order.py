from django.urls import path
from apps.views import OrderFormView, ProductSellListView, OrderListView, OrderUpdateView

urlpatterns = [
    path("order/form/<int:pk>/", OrderFormView.as_view(), name="order"),
    path("thread/market", ProductSellListView.as_view(), name="market"),
    path("order/list", OrderListView.as_view(), name="order-list"),
    path("order/detail", OrderListView.as_view(), name="order-detail"),
    path("order/update/<int:pk>", OrderUpdateView.as_view(), name="order-update"),
]