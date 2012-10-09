# Create your views here.

from core.models import *
from django.http import HttpResponse
from core.services import watch_services

def watchIssue(request, issue_id):
    watch_services.watch_issue(request.user, int(issue_id), IssueWatch.WATCHED)
    return HttpResponse("WATCHING")

def unwatchIssue(request, issue_id):
    watch_services.unwatch_issue(request.user, int(issue_id))
    return HttpResponse("UNWATCHING")

def watchOffer(request, offer_id):
    watch_services.watch_offer(request.user, int(offer_id), OfferWatch.WATCHED)
    return HttpResponse("WATCHING")

def unwatchOffer(request, offer_id):
    watch_services.unwatch_offer(request.user, int(offer_id))
    return HttpResponse("UNWATCHING")

