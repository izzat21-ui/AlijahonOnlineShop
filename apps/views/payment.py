from pyexpat.errors import messages

from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView

from apps.forms import PaymentModelForm
from apps.models import User

from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic.edit import FormView


class PaymentFormView(FormView):
    template_name = 'apps/payment/payment.html'
    form_class = PaymentModelForm
    success_url = reverse_lazy('payment')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['payments'] = self.request.user.payments.all()
        return data

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        if amount > self.request.user.balance:
            form.add_error('amount', "Mablag' yetarli emas")
            return self.form_invalid(form)
        user = self.request.user
        user.balance -= amount
        user.save()

        form.instance.user = self.request.user
        form.user = self.request.user
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        for error in form.errors.values():
            messages.error(self.request, error)
        return super().form_invalid(form)
