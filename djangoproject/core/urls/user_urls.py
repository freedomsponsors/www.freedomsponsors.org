from django.conf.urls import url
from core.views import user_views


urlpatterns = [
    # url(r'^$', 'listUsers'),
    url(r'^edit$', user_views.editUserForm, name='editUserForm'),
    url(r'^edit/submit$', user_views.editUser, name='editUser'),
    url(r'^cancel_account$', user_views.cancel_account),
    url(r'^(?P<user_id>\d+)/$', user_views.viewUserById),
    url(r'^(?P<user_id>\d+)/(?P<user_slug>.*)$', user_views.viewUserById),
    url(r'^(?P<username>.+)/$', user_views.viewUserByUsername),
]
