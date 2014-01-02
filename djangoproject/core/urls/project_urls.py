from django.conf.urls import patterns, url

urlpatterns = patterns('core.views.project_views',
    url(r'^$', 'list'),
    url(r'^(?P<project_id>\d+)/$', 'view'),
    url(r'^(?P<project_id>\d+)/edit$', 'edit_form'),
    url(r'^(?P<project_id>\d+)/.*$', 'view'),
    url(r'^submit$', 'edit'),
)
