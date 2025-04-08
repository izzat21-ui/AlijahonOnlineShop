from apps.views import ThreadRequest
from apps.views.thread import ThreadFormView, ThreadListView, ThreadStatistic
from django.urls import path

urlpatterns = [
    path("thread/form/", ThreadFormView.as_view(), name='thread-form'),
    path("thread/list", ThreadListView.as_view(), name='thread-list'),
    path("thread/statistic/", ThreadStatistic.as_view(), name='thread-statistic'),
    path("thread/request/", ThreadRequest.as_view(), name='thread-request'),
]
