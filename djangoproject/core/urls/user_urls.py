from django.conf.urls import patterns, url

urlpatterns = patterns('core.views.user_views',
    url(r'^$', 'listUsers'),
    url(r'^(?P<user_id>\d+)/$', 'viewUser'),
    url(r'^(?P<user_id>\d+)/(?P<user_slug>.*)$', 'viewUser'),
    url(r'^edit$', 'editUserForm'),
    url(r'^edit/submit$', 'editUser'),
    url(r'^cancel_account$', 'cancel_account'),
    url(r'^change_username', 'change_username'),
)
