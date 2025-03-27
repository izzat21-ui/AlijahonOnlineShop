from apps.urls.home import urlpatterns as home_url

from apps.urls.order import urlpatterns as order_url
from apps.urls.auth import urlpatterns as auth_url
from apps.urls.thread import urlpatterns as thread_url
from apps.urls.operator import urlpatterns as operator_url
from apps.urls.payment import urlpatterns as payment_url

urlpatterns = [
    *home_url,
    *order_url,
    *auth_url,
    *thread_url,
    *operator_url,
    *payment_url,
]
