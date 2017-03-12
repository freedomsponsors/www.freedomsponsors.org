# coding: utf-8
from django.conf.urls import url
from core.views import api_views

urlpatterns = [
    url(r'^project/(?P<project_id>\d+)$', api_views.get_project),
    url(r'^login$', api_views.login),
    url(r'^logout$', api_views.logout),
    url(r'^whoami$', api_views.whoami),
    url(r'^list_issues$', api_views.list_issues),
]
