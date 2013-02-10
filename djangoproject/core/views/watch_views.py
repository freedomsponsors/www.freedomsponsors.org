# Create your views here.
from django.contrib.auth.decorators import login_required
from core.models import *
from django.http import HttpResponse
from core.services import watch_services
from django.utils.translation import ugettext as _

@login_required
def watchIssue(request, issue_id):
    watch_services.watch_issue(request.user, int(issue_id), IssueWatch.WATCHED)
    return HttpResponse('WATCHING')

@login_required
def unwatchIssue(request, issue_id):
    watch_services.unwatch_issue(request.user, int(issue_id))
    return HttpResponse('NOT_WATCHING')

@login_required
def watchOffer(request, offer_id):
    watch_services.watch_offer(request.user, int(offer_id), OfferWatch.WATCHED)
    return HttpResponse('WATCHING')

@login_required
def unwatchOffer(request, offer_id):
    watch_services.unwatch_offer(request.user, int(offer_id))
    return HttpResponse('NOT_WATCHING')

