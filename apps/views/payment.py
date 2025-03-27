from django.views.generic import TemplateView


class PaymentTemplateView(TemplateView):
    template_name = 'apps/payment/payment.html'