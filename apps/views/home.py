from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, F
from django.db.models.aggregates import Count
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, FormView, ListView, DetailView
from apps.forms import AuthForm, ChangePasswordForm, ProfileForm, OrderForm
from apps.models import User, Product, Region, District, Category, Wishlist, AdminSetting, Order


class SettingsFormView(LoginRequiredMixin, FormView):
    template_name = 'apps/auth/settings.html'
    form_class = ProfileForm
    success_url = reverse_lazy('settings')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['regions'] = Region.objects.all()
        return data

    def form_valid(self, form):
        form.update(self.request.user)
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)  # Form xatolarini konsolda chiqaramiz
        return self.render_to_response(self.get_context_data(form=form))


class HomeListView(ListView):
    queryset = Category.objects.all()
    template_name = 'apps/home.html'
    context_object_name = "categories"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['products'] = Product.objects.all()
        if self.request.user.is_authenticated:
            data['liked_products_id'] = Wishlist.objects.filter(user_id=self.request.user).values_list("product_id",
                                                                                                       flat=True)
        return data


class ProductListView(ListView):
    queryset = Product.objects.all()
    template_name = 'apps/menus/product-list.html'
    context_object_name = "products"

    def get_context_data(self, *, object_list=None, **kwargs):
        slug = self.kwargs.get('slug')
        category = Category.objects.filter(slug=slug).first()
        data = super().get_context_data(object_list=object_list, **kwargs)
        products = Product.objects.all()
        if slug != 'all':
            products = products.filter(category=category)
        # -------------- search --------------
        query = self.request.GET.get('query')
        if query:
            products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
        data['products'] = products
        # -------------- search --------------

        data['categories'] = Category.objects.all()
        if self.request.user.is_authenticated:
            data['liked_products_id'] = Wishlist.objects.filter(user_id=self.request.user).values_list("product_id",
                                                                                                       flat=True)
        data['session_category'] = category
        return data


class WishlistView(LoginRequiredMixin, View):
    login_url = reverse_lazy('auth')

    def get(self, request, product_id):
        liked = True
        like = Wishlist.objects.filter(product_id=product_id, user=self.request.user)
        if like.exists():
            like.delete()
            liked = False
        else:
            Wishlist.objects.create(product_id=product_id, user=self.request.user)

        return JsonResponse({"liked": liked})


class LikeListView(ListView):
    queryset = Wishlist.objects.all()
    template_name = 'apps/menus/wish-list.html'
    context_object_name = 'products'

    def get_context_data(self, *, object_list=None, **kwargs):
        data = super().get_context_data(object_list=object_list, **kwargs)
        data['products'] = Product.objects.filter(wishlist__user=self.request.user)
        data['liked_products_id'] = Wishlist.objects.filter(user_id=self.request.user.id).values_list("product_id",
                                                                                                      flat=True)
        return data
