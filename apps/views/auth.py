from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView
from apps.forms import AuthForm, ChangePasswordForm
from apps.models import User, District


class AuthFormView(FormView):
    form_class = AuthForm
    template_name = 'apps/auth/auth.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        data = form.cleaned_data
        phone_number = data.get('phone_number')
        password = form.data.get('password')
        users = User.objects.filter(phone_number=phone_number)
        if users.exists():
            user = users.first()
            if check_password(password, user.password):
                login(self.request, user)
            else:
                messages.error(self.request, "Passwordda xatolik !")
                return redirect('auth')
        else:
            user = form.save()
            login(self.request, user)
        return super().form_valid(form)

    def form_invalid(self, form):
        for error in form.errors.values():
            messages.error(self.request, error)
        return super().form_invalid(form)


class ProfileFormView(TemplateView):
    template_name = 'apps/auth/profile.html'


class ChangePasswordFormView(LoginRequiredMixin, FormView):
    form_class = ChangePasswordForm
    template_name = 'apps/auth/auth.html'
    success_url = reverse_lazy('settings')

    def form_valid(self, form):
        session_password = self.request.user.password
        old_password = form.cleaned_data.get('old')
        if not check_password(old_password, session_password):
            messages.error(self.request, "Old Password incorrect")
        else:
            form.update(self.request.user)
        return super().form_valid(form)

    def form_invalid(self, form):
        for message in form.errors.values():
            messages.error(self.request, message)
        return redirect('settings')


def district_list_view(request):
    region_id = request.GET.get('region_id')
    districts = District.objects.filter(region_id=region_id).values("id", "name")
    return JsonResponse(list(districts), safe=False)


def logout_view(request):
    logout(request)
    return redirect("auth")
