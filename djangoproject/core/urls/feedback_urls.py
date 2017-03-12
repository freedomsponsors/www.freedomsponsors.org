# coding: utf-8
from django.conf.urls import url
from core.views import feedback_views

urlpatterns = [
    url(r'^$', feedback_views.feedback),
    url(r'^/submit$', feedback_views.addFeedback),
]
