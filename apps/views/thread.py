from django.contrib import messages
from django.db.models import Count, Q, Sum
from django.db.models.functions import Coalesce
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView, TemplateView
from apps.forms import ThreadForm
from apps.models import Thread, Product, Category, Order


class ThreadFormView(FormView):
    form_class = ThreadForm
    template_name = 'apps/thread/market-list.html'
    success_url = reverse_lazy('thread-list')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['products'] = Product.objects.all()
        data['categories'] = Category.objects.all()
        return data

    def form_valid(self, form):
        thread = form.save(commit=False)
        thread.user = self.request.user
        thread.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        for error in form.errors:
            messages.error(self.request, error)
        return super().form_invalid(form)


class ThreadListView(ListView):
    queryset = Thread.objects.all()
    template_name = 'apps/thread/thread-list.html'
    context_object_name = 'threads'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['threads'] = data.get('threads').filter(user=self.request.user).order_by('-created_at')
        return data


class ThreadStatistic(ListView):
    queryset = Thread.objects.all()
    template_name = 'apps/thread/thread-statistic.html'
    context_object_name = 'statistics'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.get_queryset().aggregate(
            all_visit_count=Sum('visit_count'),
            all_new_count=Sum('new_count'),
            all_ready_to_order_count=Sum('ready_count'),
            all_delivering_count=Sum('deliver_count'),
            all_delivered_count=Sum('delivered_count'),
            all_not_pick_up_count=Sum('cant_phone_count'),
            all_canceled_count=Sum('canceled_count'),
            all_archived_count=Sum('archived_count'),
        )
        context.update(query)
        context['thread_count'] = self.get_queryset().count()
        return context

    from django.db.models.functions import Coalesce

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user).annotate(
            new_count=Coalesce(Count('orders', filter=Q(orders__status=Order.StatusType.NEW)), 0),
            ready_count=Coalesce(Count('orders', filter=Q(orders__status=Order.StatusType.READY_TO_ORDER)), 0),
            deliver_count=Coalesce(Count('orders', filter=Q(orders__status=Order.StatusType.DELIVERING)), 0),
            delivered_count=Coalesce(Count('orders', filter=Q(orders__status=Order.StatusType.DELIVERED)), 0),
            cant_phone_count=Coalesce(Count('orders', filter=Q(orders__status=Order.StatusType.NOT_PICK_UP)), 0),
            canceled_count=Coalesce(Count('orders', filter=Q(orders__status=Order.StatusType.CANCELED)), 0),
            archived_count=Coalesce(Count('orders', filter=Q(orders__status=Order.StatusType.ARCHIVED)), 0),
        ).values(
            'name', 'product__name', 'visit_count', 'new_count',
            'ready_count', 'deliver_count', 'delivered_count',
            'cant_phone_count', 'canceled_count', 'archived_count'
        )


class ThreadRequest(TemplateView):
    template_name = 'apps/thread/thread-request.html'
