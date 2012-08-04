from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

urlpatterns = patterns('core.views',
	url(r'^$', 'home'),
	url(r'^home/$', 'home'),
	url(r'^about/$', TemplateView.as_view(template_name='core/about.html')),
	url(r'^faq/$', TemplateView.as_view(template_name='core/faq.html')),
	url(r'^dev/$', TemplateView.as_view(template_name='core/dev.html')),
	url(r'^myissues/$', 'myissues'),
	url(r'^user/(?P<user_id>\d+)/$', 'viewUser'),
	url(r'^user/(?P<user_id>\d+)/history*$', 'viewUserHistory'),
	url(r'^user/(?P<user_id>\d+)/.*$', 'viewUser'),
	url(r'^user/edit$', 'editUserForm'),
	url(r'^user/edit/submit$', 'editUser'),
	url(r'^project/$', 'listProjects'),
	url(r'^issue/$', 'listIssues'),
    url(r'^issue/(?P<issue_id>\d+)/$', 'viewIssue'),
    url(r'^issue/(?P<issue_id>\d+)/.*$', 'viewIssue'),
	url(r'^issue/add/$', 'addIssueForm'),
	url(r'^issue/sponsor$', 'addIssueForm'),
	url(r'^issue/add/submit$', 'addIssue'),
	url(r'^issue/sponsor/submit$', 'sponsorIssue'),
	url(r'^issue/comment/add/submit$', 'addIssueComment'),
	url(r'^issue/comment/edit/submit$', 'editIssueComment'),
    url(r'^offer/(?P<offer_id>\d+)/$', 'viewOffer'),
	url(r'^offer/(?P<offer_id>\d+)/pay$', 'payOfferForm'),
	url(r'^offer/(?P<offer_id>\d+)/.*$', 'viewOffer'),
    url(r'^offer/pay/submit$', 'payOffer'),
	url(r'^offer/comment/add/submit$', 'addOfferComment'),
	url(r'^offer/comment/edit/submit$', 'editOfferComment'),
	url(r'^offer/revoke/submit$', 'revokeOffer'),
	url(r'^offer/edit/submit$', 'editOffer'),
	url(r'^paypal/cancel$', 'paypalCancel'),
	url(r'^paypal/return$', 'paypalReturn'),
	url(r'^paypal/megablasteripn$', 'paypalIPN'),
	url(r'^solution/add/submit$', 'addSolution'),
	url(r'^solution/abort/submit$', 'abortSolution'),
	url(r'^solution/resolve/submit$', 'resolveSolution'),
	url(r'^login/$', 'login'),
	url(r'^logout/$', 'logout'),
)

urlpatterns += patterns('core.jsonviews',
	url(r'^json/project$', 'project'),
	url(r'^json/by_issue_url$', 'by_issue_url'),
	url(r'^json/get_offers$', 'get_offers'),
)

# urlpatterns += patterns('core.jiraviews',
# 	url(r'^issue/sponsor_jira$', 'sponsorJiraForm'),
# )

urlpatterns += patterns('core.feedbackviews',
	url(r'^feedback$', 'feedback'),
	url(r'^feedback/submit$', 'addFeedback'),
)


