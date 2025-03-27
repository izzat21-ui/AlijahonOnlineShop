from django.contrib import admin
from apps.models import User, Product, Category, Region, AdminSetting


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    exclude = 'slug',


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    pass

@admin.register(AdminSetting)
class SettingAdmin(admin.ModelAdmin):
    pass


