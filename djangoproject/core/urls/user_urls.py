from django.conf.urls import patterns, url

urlpatterns = patterns('core.views.user_views',
    # url(r'^$', 'listUsers'),
    url(r'^edit$', 'editUserForm'),
    url(r'^edit/submit$', 'editUser'),
    url(r'^cancel_account$', 'cancel_account'),
    url(r'^(?P<user_id>\d+)/$', 'viewUserById'),
    url(r'^(?P<user_id>\d+)/(?P<user_slug>.*)$', 'viewUserById'),
    url(r'^(?P<username>.+)/$', 'viewUserByUsername'),
)
