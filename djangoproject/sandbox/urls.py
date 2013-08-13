from django.conf.urls import patterns, url
from django.views.generic.simple import redirect_to, direct_to_template

__author__ = 'tony'

urlpatterns = patterns('sandbox.views',
    url(r'^$', direct_to_template, {'template': 'sandbox/home.html'}),
    url(r'^issue_page$', direct_to_template, {'template': 'sandbox/issue_page.html'}),
    # url(r'^home/$', 'home'),
)
