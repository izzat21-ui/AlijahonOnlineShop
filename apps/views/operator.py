from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, DetailView

from apps.models import Order, Category, Region, District



class OperatorTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'apps/operator/operator-page.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.role == 'operator':
            return super().dispatch(request, *args, **kwargs)

        elif self.request.user.role == 'deliver':
            return super().dispatch(request, *args, **kwargs)
        return redirect('home')

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, 'apps/operator/operator-page.html', context)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        status = self.request.GET.get("status")
        category_id = self.request.POST.get('category_id')
        district_id = self.request.POST.get('district_id')

        data['categories'] = Category.objects.all()
        data['regions'] = Region.objects.all()

        # Role asosida statuslar
        action_map = {
            "operator": ['new', 'pending', 'canceled', 'not_pick_up', 'archived'],
            "deliver": ['delivering', 'delivered', 'completed', 'ready_to_order']
        }

        orders = Order.objects.all()

        if status:
            if status == "new":
                orders = orders.filter(status=status)
            else:
                orders = orders.filter(operator=self.request.user, status=status)
        else:
            if self.request.user.role == 'deliver':
                orders = orders.filter(status='ready_to_order')

        if category_id:
            orders = orders.filter(product__category_id=category_id)
        if district_id:
            orders = orders.filter(district_id=district_id)

        data["status"] = action_map.get(self.request.user.role)
        data['orders'] = orders

        return data


class OperatorOrderChangeDetailView(DetailView):
    queryset = Order.objects.all()
    template_name = 'apps/operator/order-change.html'
    pk_url_kwarg = 'pk'
    context_object_name = 'order'

    def get(self, request, *args, **kwargs):
        order_id = kwargs.get('pk')

        Order.objects.filter(pk=order_id).update(operator=request.user)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['regions'] = Region.objects.all()
        return data
