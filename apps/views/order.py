from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, F
from django.db.models.aggregates import Count
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView, DetailView, UpdateView
from apps.forms import OrderForm, OrderModelForm
from apps.models import User, Product, Category, AdminSetting, Order


class ProductSellListView(ListView):
    queryset = Product.objects.all()
    template_name = "apps/thread/market-list.html"
    context_object_name = "products"

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(object_list=object_list, **kwargs)
        products = data['products']
        slug = self.request.GET.get('category')
        if slug == 'top':
            products = Product.objects.annotate(order_count=Count(F('orders'))).order_by('order_count')[:10]
        elif slug != 'all':
            products = Product.objects.filter(category__slug=slug)
        data['products'] = products
        data['categories'] = Category.objects.all()
        return data


class CompetitionListView(ListView):
    queryset = User.objects.all()
    template_name = 'apps/menus/competition.html'
    context_object_name = "users"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['site'] = AdminSetting.objects.first()
        return data

    def get_queryset(self):
        query = super().get_queryset()
        query = query.annotate(
            order_count=Count('thread__orders', filter=Q(thread__orders__status=Order.StatusType.COMPLETED))).order_by(
            "-order_count").order_by("-order_count").only('first_name')
        return query


class ProductDetailView(DetailView):
    queryset = Product.objects.all()
    template_name = 'apps/order/product-detail.html'
    slug_url_kwarg = "slug"
    context_object_name = "product"


class OrderFormView(FormView):
    form_class = OrderForm
    success_url = reverse_lazy('order')

    def form_valid(self, form):
        order = form.save(self.request.user)
        deliver_price = AdminSetting.objects.first().deliver_price
        return render(self.request, 'apps/order/order-success.html',
                      context={"order": order, "deliver_price": deliver_price})

    def form_invalid(self, form):
        pass


class OrderListView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('auth')
    queryset = Order.objects.all()
    template_name = 'apps/order/order-list.html'
    context_object_name = "orders"

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(object_list=object_list, **kwargs)
        data['orders'] = data.get('orders').filter(owner=self.request.user)
        return data


class OrderUpdateView(UpdateView):
    queryset = Order.objects.all()
    form_class = OrderModelForm
    template_name = 'apps/operator/order-change.html'
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('operator')













































