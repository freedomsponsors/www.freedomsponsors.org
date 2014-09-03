# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from core.models import *
from django.http import HttpResponse
from django.utils.translation import ugettext as _
import json
from core.services import issue_services, tag_services, activity_services, watch_services, mail_services, user_services
import traceback
import logging
from django.contrib.auth.decorators import login_required

logger = logging.getLogger(__name__)


def project(request):
    if 'query' in request.GET:
        query = request.GET['query']
        projects = Project.objects.filter(name__istartswith=query)[:5]
        result = []
        for project in projects:
            result.append({"id": project.id, "value": project.name})
        return HttpResponse(json.dumps(result))
    else:
        return HttpResponse(_("Error: need query parameter."), status=404)


def by_issue_url(request):
    if 'trackerURL' in request.GET:
        trackerURL = request.GET['trackerURL']
        try:
            result = issue_services.process_issue_url(trackerURL, request.user)
            return HttpResponse(json.dumps(result))
        except:
            traceback.print_exc()
            raise
    else:
        return HttpResponse(_("Error: need trackerURL parameter."), status=404)


def get_offers(request):
    trackerURL = request.GET.get('trackerURL')
    if not trackerURL:
        return HttpResponse(_("Error: need trackerURL parameter."), status=404)
    sponsor_id = request.GET.get('sponsor_id')
    offers = Offer.objects.filter(issue__trackerURL__iexact=trackerURL)
    if sponsor_id:
        offers = offers.filter(sponsor__id=int(sponsor_id))
    return HttpResponse(json.dumps(_convert_offers_to_dict(offers)))


def list_issue_cards(request):
    project_id = None
    if 'project_id' in request.GET:
        project_id = int(request.GET.get('project_id'))
    offset = int(request.GET.get('offset'))
    count = int(request.GET.get('count'))
    if not count:
        count = 3
    is_sponsored = request.GET.get('sponsoring').lower() == 'true'
    count = min(count, 100)
    query = issue_services.search_issues(project_id=project_id, is_sponsored=is_sponsored)
    total_count = query.count()
    issues = query[offset: offset + count]
    issues = issue_services.to_card_dict(issues)
    result = {
        'count': total_count,
        'issues': issues
    }
    return HttpResponse(json.dumps(result))


@login_required
def add_tag(request):
    name = request.POST.get('name')
    objtype = request.POST.get('objtype')
    objid = int(request.POST.get('objid'))
    if not objtype in ['Project', 'Issue']:
        raise BaseException('Wrong objtype: %s' % objtype)
    tag_services.addTag(name, objtype, objid)
    _project = Project.objects.get(pk=objid)
    watches = watch_services.find_project_watches(_project)  #TODO: in the future, not only projects!
    mail_services.notifyWatchers_project_tag_added(request.user, _project, name, watches)
    ActionLog.log_project_tag_added(user=request.user, project_id=objid, tag_name=name)
    return HttpResponse('')


@login_required
def remove_tag(request):
    name = request.POST.get('name')
    objtype = request.POST.get('objtype')
    objid = int(request.POST.get('objid'))
    tag_services.removeTag(name, objtype, objid)
    _project = Project.objects.get(pk=objid)
    watches = watch_services.find_project_watches(_project)
    mail_services.notifyWatchers_project_tag_removed(request.user, _project, name, watches)
    ActionLog.log_project_tag_removed(user=request.user, project_id=objid, tag_name=name)
    return HttpResponse('')


@login_required
def toggle_watch(request):
    objid = int(request.POST.get('objid'))
    entity = request.POST.get('entity')
    watching = watch_services.toggle_watch(request.user, entity, objid, Watch.WATCHED)
    return HttpResponse('WATCHING' if watching else 'NOT_WATCHING')


def latest_activity(request):
    project_id = int(request.GET.get('project_id')) if 'project_id' in request.GET else None
    offset = int(request.GET.get('offset'))
    activities, count = activity_services.get_latest_activity(project_id, offset)
    result = {
        'count': count,
        'activities': [activity.to_dict_json() for activity in activities],
    }
    return HttpResponse(json.dumps(result))


@login_required
def check_username_availability(request, username):
    if username == request.user.username:
        result = {
            'ok': False,
            'message': '"%s" is already your current username!' % username
        }
    elif not user_services.is_valid_username(username):
        result = {
            'ok': False,
            'message': 'Sorry! "%s" is not a valid username (should be alphanumeric).' % username
        }
    elif not user_services.is_username_available(username):
        result = {
            'ok': False,
            'message': 'Sorry, "%s" is already taken.' % username
        }
    else:
        result = {
            'ok': True,
            'message': 'Great! "%s" is available!' % username
        }
    return HttpResponse(json.dumps(result))


def _convert_offers_to_dict(offers):
    result = []
    for offer in offers:
        result.append({
            'id': offer.id,
            'issue_id': offer.issue.id,
            'sponsor_id': offer.sponsor.id,
            'creationDate': str(offer.creationDate),
            'lastChangeDate': str(offer.lastChangeDate),
            'price': str(offer.price),
            'no_forking': str(offer.no_forking),
            'require_release': str(offer.require_release),
            'status': offer.status})
    return result






