from django.conf.urls import patterns, url
from django.views.generic.simple import redirect_to, direct_to_template

__author__ = 'tony'

urlpatterns = patterns('sandbox.views',
    url(r'^$', direct_to_template, {'template': 'sandbox/home.html'}),
    url(r'^issue_page$', direct_to_template, {'template': 'sandbox/issue_page.html'}),
    url(r'^user_page$', direct_to_template, {'template': 'sandbox/user.html'}),
	url(r'^search_page$', direct_to_template, {'template': 'sandbox/search.html'}), 
    url(r'^adropdown', direct_to_template, {'template': 'sandbox/adropdown.html'}),
    url(r'^atabnav', direct_to_template, {'template': 'sandbox/atabnav.html'}),
    url(r'^amodal', direct_to_template, {'template': 'sandbox/amodal.html'}),
    url(r'^apopover', direct_to_template, {'template': 'sandbox/apopover.html'}),
    # url(r'^home/$', 'home'),
)
