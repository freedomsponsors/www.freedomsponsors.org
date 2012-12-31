from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.conf import settings

urlpatterns = patterns('core.views.main_views',
    url(r'^stats/$', 'stats'),
    url(r'^admail/$', 'admail'),
    url(r'^about/$', TemplateView.as_view(template_name='core/about.html')),
    url(r'^faq/$', TemplateView.as_view(template_name='core/faq.html')),
    url(r'^dev/$', TemplateView.as_view(template_name='core/dev.html')),
    url(r'^login/$', 'login'),
    url(r'^logout/$', 'logout'),
)

urlpatterns += patterns('core.views.issue_views',
    url(r'^project/$', 'listProjects'),
    url(r'^myissues/$', 'myissues'),
    url(r'^issue/$', 'listIssues'),
    url(r'^issue/sponsor/submit$', 'sponsorIssue'),
    url(r'^issue/sponsor$', 'addIssueForm'),
    url(r'^issue/add/submit$', 'addIssue'),
    url(r'^issue/kickstart/submit$', 'kickstartIssue'),
    url(r'^issue/add/$', 'addIssueForm'),
    url(r'^offer/(?P<offer_id>\d+)/pay$', 'payOfferForm'),
    url(r'^issue/(?P<issue_id>\d+)/$', 'viewIssue'),
    url(r'^issue/(?P<issue_id>\d+)/.*$', 'viewIssue'),
    url(r'^offer/(?P<offer_id>\d+)/$', 'viewOffer'),
    url(r'^offer/(?P<offer_id>\d+)/.*$', 'viewOffer'),
    url(r'^offer/revoke/submit$', 'revokeOffer'),
    url(r'^offer/edit/submit$', 'editOffer'),
    url(r'^solution/add/submit$', 'addSolution'),
    url(r'^solution/abort/submit$', 'abortSolution'),
    url(r'^solution/resolve/submit$', 'resolveSolution'),
)

urlpatterns += patterns('core.views.comment_views',
    url(r'^issue/comment/add/submit$', 'addIssueComment'),
    url(r'^issue/comment/edit/submit$', 'editIssueComment'),
    url(r'^issue/comment/(?P<comment_id>\d+)/history$', 'viewIssueCommentHistory'),
    url(r'^offer/comment/add/submit$', 'addOfferComment'),
    url(r'^offer/comment/edit/submit$', 'editOfferComment'),
    url(r'^offer/comment/(?P<comment_id>\d+)/history$', 'viewOfferCommentHistory'),
)

urlpatterns += patterns('core.views.watch_views',
    url(r'^watch/issue/(?P<issue_id>\d+)$', 'watchIssue'),
    url(r'^unwatch/issue/(?P<issue_id>\d+)$', 'unwatchIssue'),
    url(r'^watch/offer/(?P<offer_id>\d+)$', 'watchOffer'),
    url(r'^unwatch/offer/(?P<offer_id>\d+)$', 'unwatchOffer'),
)

urlpatterns += patterns('core.views.paypal_views',
    url(r'^offer/pay/submit$', 'payOffer'),
    url(r'^paypal/cancel$', 'paypalCancel'),
    url(r'^paypal/return$', 'paypalReturn'),
    url(r'^paypal/'+settings.PAYPAL_IPNNOTIFY_URL_TOKEN+'$', 'paypalIPN'),
)

urlpatterns += patterns('core.views.user_views',
    url(r'^user/$', 'listUsers'),
    url(r'^user/(?P<user_id>\d+)/$', 'viewUser'),
    url(r'^user/(?P<user_id>\d+)/.*$', 'viewUser'),
    url(r'^user/edit$', 'editUserForm'),
    url(r'^user/edit/submit$', 'editUser'),
)

urlpatterns += patterns('core.views.json_views',
    url(r'^json/project$', 'project'),
    url(r'^json/by_issue_url$', 'by_issue_url'),
    url(r'^json/get_offers$', 'get_offers'),
)

# urlpatterns += patterns('core.jiraviews',
#   url(r'^issue/sponsor_jira$', 'sponsorJiraForm'),
# )

urlpatterns += patterns('core.views.feedback_views',
    url(r'^feedback$', 'feedback'),
    url(r'^feedback/submit$', 'addFeedback'),
)


