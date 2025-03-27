from django.urls import path
from apps.views import AuthFormView, SettingsFormView, ProfileFormView, \
    district_list_view, ChangePasswordFormView, logout_view

urlpatterns = [
    path("auth/", AuthFormView.as_view(), name="auth"),
    path("profile/settings/", SettingsFormView.as_view(), name="settings"),
    path("profile/", ProfileFormView.as_view(), name="profile"),
    path("district-list/", district_list_view, name="district-list"),
    path("change-password/", ChangePasswordFormView.as_view(), name="change-password"),
    path("logout/", logout_view, name="logout"),
]
