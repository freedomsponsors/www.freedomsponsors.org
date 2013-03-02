# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from views import email_add, email_list, email_delete, \
            email_send_activation, email_activate, email_make_primary

#add an email to a User account
urlpatterns = patterns('',
    url(
        r'^email/add/$', 
        email_add, 
        name='emailmgr_email_add'
        ),
    url(
        r'^email/send_activation/(?P<identifier>\w+)/$',
        email_send_activation,
        name='emailmgr_email_send_activation'
        ),
    url(
        r'^email/activate/(?P<identifier>\w+)/$',
        email_activate,
        name='emailmgr_email_activate'
        ),
    url(
        r'^email/make_primary/(?P<identifier>\w+)/$',
        email_make_primary,
        name='emailmgr_email_make_primary'
        ),
    url(
        r'^email/delete/(?P<identifier>\w+)/$',
        email_delete,
        name='emailmgr_email_delete'
        ),
    url(
        r'^email/$',
        email_list,
        name='emailmgr_email_list'
        ),
)