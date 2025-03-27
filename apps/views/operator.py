from django.shortcuts import render
from django.views.generic import TemplateView, DetailView

from apps.models import Order, Category, Region, District


class OperatorTemplateView(TemplateView):
    template_name = 'apps/operator/operator-page.html'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, 'apps/operator/operator-page.html', context)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        status = self.request.GET.get('status')
        category_id = self.request.POST.get('category_id')
        district_id = self.request.POST.get('district_id')
        data['status'] = Order.StatusType.values
        data['categories'] = Category.objects.all()
        data['regions'] = Region.objects.all()
        orders = Order.objects.filter(status=Order.StatusType.NEW)
        if status:
            orders = Order.objects.filter(status=status)
        if category_id:
            orders = orders.filter(product__category_id=category_id)
        if district_id:
            orders = orders.filter(district_id=district_id)
        data['orders'] = orders
        return data


class OperatorOrderChangeDetailView(DetailView):
    queryset = Order.objects.all()
    template_name = 'apps/operator/order-change.html'
    pk_url_kwarg = 'pk'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['regions'] = Region.objects.all()
        return data