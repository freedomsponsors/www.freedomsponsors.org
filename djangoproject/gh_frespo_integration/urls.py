from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.conf import settings

urlpatterns = patterns('gh_frespo_integration.views.main_views',
    url(r'^configure/$', 'configure'),
    url(r'^configure/submit/$', 'configure_submit'),
)

