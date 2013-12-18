from django.conf.urls import patterns, url
from django.views.generic.simple import direct_to_template

__author__ = 'tony'

urlpatterns = patterns('sandbox.views',
    url(r'^$', 'home'),
    url(r'^faq$', direct_to_template, {'template': 'core2/faq.html'}),
    url(r'^issue$', 'issue'),
    url(r'^user_page$', direct_to_template, {'template': 'sandbox/user.html'}),
	url(r'^search_page$', direct_to_template, {'template': 'sandbox/search.html'}),
	url(r'^project_page$', direct_to_template, {'template': 'sandbox/project.html'}), 	
    url(r'^adropdown', direct_to_template, {'template': 'sandbox/adropdown.html'}),
    url(r'^atabnav', direct_to_template, {'template': 'sandbox/atabnav.html'}),
    url(r'^amodal', direct_to_template, {'template': 'sandbox/amodal.html'}),
    url(r'^apopover', direct_to_template, {'template': 'sandbox/apopover.html'}),
    # url(r'^home/$', 'home'),
)
