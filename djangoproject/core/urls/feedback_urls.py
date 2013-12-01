# coding: utf-8
from django.conf.urls import patterns, url

urlpatterns = patterns('core.views.feedback_views',
    url(r'^$', 'feedback'),
    url(r'^/submit$', 'addFeedback'),
)
