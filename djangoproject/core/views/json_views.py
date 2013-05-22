# Create your views here.

from core.models import *
from django.http import HttpResponse
from django.utils.translation import ugettext as _
import json
from core.services import issue_services
import traceback
import logging

logger = logging.getLogger(__name__)

def project(request):
    if request.GET.has_key('query'):
        query = request.GET['query']
        projects = Project.objects.filter(name__istartswith=query)[:5]
        result = []
        for project in projects:
            result.append({"id":project.id, "value":project.name})
        return HttpResponse(json.dumps(result))
    else :
        return HttpResponse(_("Error: need query parameter."), status=404)

def by_issue_url(request):
    if request.GET.has_key('trackerURL'):
        trackerURL = request.GET['trackerURL']
        try:
            result = issue_services.process_issue_url(trackerURL, request.user)
            return HttpResponse(json.dumps(result))
        except:
            traceback.print_exc()
            raise
    else :
        return HttpResponse(_("Error: need trackerURL parameter."), status=404)

def get_offers(request):
    trackerURL = request.GET.get('trackerURL')
    if(not trackerURL):
        return HttpResponse(_("Error: need trackerURL parameter."), status=404)
    sponsor_id = request.GET.get('sponsor_id')
    offers = Offer.objects.filter(issue__trackerURL__iexact=trackerURL)
    if(sponsor_id):
        offers = offers.filter(sponsor__id=int(sponsor_id))
    return HttpResponse(json.dumps(_convert_offers_to_dict(offers)))

def _convert_offers_to_dict(offers):
    result = []
    for offer in offers:
        result.append({
            'id' : offer.id,
            'issue_id' : offer.issue.id,
            'sponsor_id' : offer.sponsor.id,
            'creationDate' : str(offer.creationDate),
            'lastChangeDate' : str(offer.lastChangeDate),
            'price' : str(offer.price),
            'no_forking' : str(offer.no_forking),
            'require_release' : str(offer.require_release),
            'status' : offer.status})
    return result









