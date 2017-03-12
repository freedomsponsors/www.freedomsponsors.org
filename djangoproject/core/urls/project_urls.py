from django.conf.urls import url
from core.views import project_views


urlpatterns = [
    url(r'^$', project_views.list),
    url(r'^(?P<project_id>\d+)/$', project_views.view),
    url(r'^(?P<project_id>\d+)/edit$', project_views.edit_form),
    url(r'^(?P<project_id>\d+)/.*$', project_views.view),
    url(r'^submit$', project_views.edit),
]
