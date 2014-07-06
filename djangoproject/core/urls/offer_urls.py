from django.conf.urls import patterns, url

urlpatterns = patterns('core.views.issue_views',
    url(r'^(?P<offer_id>\d+)/pay$', 'payOfferForm'),
    url(r'^pay/submit$', 'payOffer'),
    url(r'^revoke/submit$', 'revokeOffer'),
    url(r'^edit/submit$', 'editOffer'),
)

urlpatterns += patterns('core.views.comment_views',
    url(r'^comment/(?P<comment_id>\d+)/history$', 'viewOfferCommentHistory'),
)

