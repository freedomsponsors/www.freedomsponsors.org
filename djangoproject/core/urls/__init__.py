from django.conf.urls import include, url
from django.views.generic import TemplateView, RedirectView
from django.conf import settings
from core.views import main_views
from core.views import paypal_views
from core.views import bitcoin_views
from core.views import json_views

urlpatterns = [
    url(r'^$', main_views.home),
    url(r'^admail/$', main_views.admail),
    url(r'^mailtest/$', main_views.mailtest),
    url(r'^about/$', RedirectView.as_view(url='http://blog.freedomsponsors.org/about/')),
    url(r'^dev/$', RedirectView.as_view(url='/developers/')),
]

# 301 redirects
urlpatterns += [
    url(r'^home/$',    RedirectView.as_view(url='/',         permanent=True)),
    url(r'^faq$',      RedirectView.as_view(url='/faq',      permanent=True)),
    url(r'^jslic$',    RedirectView.as_view(url='/jslic',    permanent=True)),
    url(r'^stats$',    RedirectView.as_view(url='/stats',    permanent=True)),
    url(r'^feedback$', RedirectView.as_view(url='/feedback', permanent=True)),

    url(r'^issue/$',              RedirectView.as_view(url='/search/',        permanent=True, query_string=True)),
    url(r'^issue/(?P<temp>.*)$',  RedirectView.as_view(url='/issue/%(temp)s', permanent=True, query_string=True)),

    url(r'^project/$',                         RedirectView.as_view(url='/project/', permanent=True)),
    url(r'^project/(?P<project_id>\d+)/$',     RedirectView.as_view(url='/project/%(project_id)s/', permanent=True)),
    url(r'^project/(?P<project_id>\d+)/edit$', RedirectView.as_view(url='/project/%(project_id)s/edit', permanent=True)),

    # url(r'^user/$',                                   RedirectView.as_view(url='/user/', permanent=True)),
    url(r'^user/(?P<user_id>\d+)/$',                  RedirectView.as_view(url='/user/%(user_id)s/', permanent=True)),
    url(r'^user/(?P<user_id>\d+)/(?P<user_slug>.*)$', RedirectView.as_view(url='/user/%(user_id)s/%(user_slug)s', permanent=True)),
]

urlpatterns += [
    url(r'^paypal/cancel$', paypal_views.paypalCancel),
    url(r'^paypal/return$', paypal_views.paypalReturn),
    url(r'^paypal/'+settings.PAYPAL_IPNNOTIFY_URL_TOKEN+'$', paypal_views.paypalIPN),
]

urlpatterns += [
    url(r'^bitcoin/'+settings.BITCOIN_IPNNOTIFY_URL_TOKEN+'$', bitcoin_views.bitcoinIPN),
]

urlpatterns += [
    url(r'^json/project$', json_views.project),
    url(r'^json/by_issue_url$', json_views.by_issue_url),
    url(r'^json/get_offers$', json_views.get_offers),
    url(r'^json/list_issue_cards', json_views.list_issue_cards),
    url(r'^json/add_tag', json_views.add_tag),
    url(r'^json/remove_tag', json_views.remove_tag),
    url(r'^json/latest_activity', json_views.latest_activity),
    url(r'^json/toggle_watch', json_views.toggle_watch),
    url(r'^json/check_username_availability/(?P<username>.+)', json_views.check_username_availability),
]
