from django.conf.urls import url
from core.views import issue_views

urlpatterns = [
    url(r'^(?P<offer_id>\d+)/pay$', issue_views.payOfferForm),
    url(r'^pay/submit$', issue_views.payOffer),
    url(r'^revoke/submit$', issue_views.revokeOffer),
    url(r'^edit/submit$', issue_views.editOffer),
]
