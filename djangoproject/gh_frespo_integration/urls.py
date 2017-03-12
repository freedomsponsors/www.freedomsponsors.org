from django.conf.urls import include, url
from django.views.generic import TemplateView
from django.conf import settings
from gh_frespo_integration.views import main_views

urlpatterns = [
    url(r'^configure/$', main_views.configure),
    url(r'^configure/submit/$', main_views.configure_submit),
]

