from django.conf.urls import patterns, url

urlpatterns = patterns('core.views.watch_views',
    url(r'^issue/(?P<issue_id>\d+)/watch$', 'watchIssue'),
    url(r'^issue/(?P<issue_id>\d+)/unwatch$', 'unwatchIssue'),
)

