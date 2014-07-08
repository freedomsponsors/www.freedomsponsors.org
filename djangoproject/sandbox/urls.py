from django.conf.urls import patterns, url
from django.views.generic import TemplateView

__author__ = 'tony'

urlpatterns = patterns('sandbox.views',
    url(r'^$', 'home'),
    url(r'^issue$', 'issue'),
    url(r'^project_edit', TemplateView.as_view(template_name='core2/project_edit.html')),
    url(r'^project', 'project'),
    # url(r'^project_page$', TemplateView.as_view(template_name='sandbox/project.html')),
    url(r'^faq$', TemplateView.as_view(template_name='core2/faq.html')),
    url(r'^user_page$', TemplateView.as_view(template_name='sandbox/user.html')),
	url(r'^search_page$', TemplateView.as_view(template_name='sandbox/search.html')),
    url(r'^adropdown', TemplateView.as_view(template_name='sandbox/adropdown.html')),
    url(r'^atabnav', TemplateView.as_view(template_name='sandbox/atabnav.html')),
    url(r'^amodal', TemplateView.as_view(template_name='sandbox/amodal.html')),
    url(r'^apopover', TemplateView.as_view(template_name='sandbox/apopover.html')),
)
