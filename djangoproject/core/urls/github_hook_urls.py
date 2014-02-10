from django.conf.urls import patterns, url

urlpatterns = patterns('core.views.github_hook_views',
    url(r'^(?P<token>\w+)/$', 'hook'),
)
