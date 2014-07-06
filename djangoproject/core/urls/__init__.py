from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView, RedirectView
from django.conf import settings
from django.views.generic.simple import redirect_to, direct_to_template

urlpatterns = patterns('core.views.main_views',
    url(r'^$', 'home'),
    url(r'^home/$', RedirectView.as_view(url='/', permanent=True)),
    url(r'^toggle_layout/$', 'toggle_layout'),
    url(r'^stats/$', 'stats'),
    url(r'^admail/$', 'admail'),
    url(r'^mailtest/$', 'mailtest'),
    url(r'^about/$', redirect_to, {'url': 'http://blog.freedomsponsors.org/about/'}),
    url(r'^faq/$', redirect_to, {'url': 'http://blog.freedomsponsors.org/faq/'}),
    url(r'^dev/$', redirect_to, {'url': 'http://blog.freedomsponsors.org/developers/'}),
    url(r'^login/$', 'login'),
    url(r'^logout/$', 'logout'),
    url(r'^jslic$', direct_to_template, {'template': 'core/jslic.html'}),
)

urlpatterns += patterns('core.views.issue_views',
    url(r'^myissues/$', 'myissues'),
    url(r'^solution/add/submit$', 'addSolution'),
    url(r'^solution/abort/submit$', 'abortSolution'),
    url(r'^solution/resolve/submit$', 'resolveSolution'),
)

# below url redirections ensure existing/external links to /core/issue/* urls still work
urlpatterns += patterns('',
    url(r'^issue/$',              RedirectView.as_view(url='/search/',        permanent=True, query_string=True)),
    url(r'^issue/(?P<temp>.*)$',  RedirectView.as_view(url='/issue/%(temp)s', permanent=True, query_string=True)),
)

urlpatterns += patterns('',
    url(r'^project/$', RedirectView.as_view(url='/project/', permanent=True)),
    url(r'^project/(?P<project_id>\d+)/$', RedirectView.as_view(url='/project/%(project_id)s/', permanent=True)),
    url(r'^project/(?P<project_id>\d+)/edit$', RedirectView.as_view(url='/project/%(project_id)s/edit', permanent=True)),
)

# below url redirections ensure existing/external links to /core/offer/* urls still work
urlpatterns += patterns('',
    url(r'^offer/(?P<temp>.*)$',  RedirectView.as_view(url='/offer/%(temp)s', permanent=True, query_string=True)),
)

urlpatterns += patterns('', # TODO: how to use reverse_lazy here?
    url(r'^watch/issue/(?P<issue_id>\d+)$', RedirectView.as_view(url='/issue/%(issue_id)s/watch', permanent=True)),
    url(r'^unwatch/issue/(?P<issue_id>\d+)$', RedirectView.as_view(url='/issue/%(issue_id)s/unwatch', permanent=True)),
    url(r'^watch/offer/(?P<offer_id>\d+)$', RedirectView.as_view(url='/offer/%(offer_id)s/watch', permanent=True)),
    url(r'^unwatch/offer/(?P<offer_id>\d+)$', RedirectView.as_view(url='/offer/%(offer_id)s/unwatch', permanent=True)),
)

urlpatterns += patterns('core.views.paypal_views',
    url(r'^paypal/cancel$', 'paypalCancel'),
    url(r'^paypal/return$', 'paypalReturn'),
    url(r'^paypal/'+settings.PAYPAL_IPNNOTIFY_URL_TOKEN+'$', 'paypalIPN'),
)

urlpatterns += patterns('core.views.bitcoin_views',
    url(r'^bitcoin/'+settings.BITCOIN_IPNNOTIFY_URL_TOKEN+'$', 'bitcoinIPN'),
)

urlpatterns += patterns('',
    url(r'^user/$', RedirectView.as_view(url='/user/', permanent=True)),
    url(r'^user/(?P<user_id>\d+)/$', RedirectView.as_view(url='/user/%(user_id)s/', permanent=True)),
    url(r'^user/(?P<user_id>\d+)/(?P<user_slug>.*)$', RedirectView.as_view(url='/user/%(user_id)s/%(user_slug)s', permanent=True)),
    url(r'^user/edit$', RedirectView.as_view(url='/user/edit', permanent=True)),
)

urlpatterns += patterns('core.views.json_views',
    url(r'^json/project$', 'project'),
    url(r'^json/by_issue_url$', 'by_issue_url'),
    url(r'^json/get_offers$', 'get_offers'),
    url(r'^json/list_issue_cards', 'list_issue_cards'),
    url(r'^json/add_tag', 'add_tag'),
    url(r'^json/remove_tag', 'remove_tag'),
    url(r'^json/latest_activity', 'latest_activity'),
    url(r'^json/toggle_watch', 'toggle_watch'),
)

# urlpatterns += patterns('core.jiraviews',
#   url(r'^issue/sponsor_jira$', 'sponsorJiraForm'),
# )

urlpatterns += patterns('',
    url(r'^feedback$', RedirectView.as_view(url='/feedback', permanent=True)),
)
