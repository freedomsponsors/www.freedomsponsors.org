from django.conf.urls import url
from core.views import payment_views

urlpatterns = [
    url(r'^$', payment_views.list_payments),
    url(r'^(?P<payment_id>\d+)/$', payment_views.view_payment),
]
