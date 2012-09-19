# Create your views here.

from core.models import *
from django.http import HttpResponse
from core.frespoutils import validateIssueURL, dictOrEmpty
import json
import logging
from core.trackerutils import fetchIssueInfo
from core.frespomail import notify_admin
import traceback


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
        return HttpResponse("Error: need query parameter.", status=404)

def by_issue_url(request):
    if request.GET.has_key('trackerURL'):
        trackerURL = request.GET['trackerURL']
        try:
            result = _process_issue_url(trackerURL, request.user)
            return HttpResponse(json.dumps(result))
        except:
            traceback.print_exc()
            raise
    else :
        return HttpResponse("Error: need trackerURL parameter.", status=404)

def get_offers(request):
    trackerURL = dictOrEmpty(request.GET, 'trackerURL')
    if(not trackerURL):
        return HttpResponse("Error: need trackerURL parameter.", status=404)
    sponsor_id = dictOrEmpty(request.GET, 'sponsor_id')
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

def _process_issue_url(trackerURL, user):
    result = {}
    result["urlValidationError"] = validateIssueURL(trackerURL)
    if(not result["urlValidationError"]):
        issues = Issue.objects.filter(trackerURL__iexact=trackerURL)
        issue_already_exists = issues.count() >= 1
        if(issues.count() > 1):
            logger.warning("Database inconsistency: more than one issue found with url = %s"%trackerURL)
        if(issue_already_exists):
            result["issue"] = {"id":issues[0].id}
            return result
        else:
            issueInfo = fetchIssueInfo(trackerURL)
            _append_project_id_and_update_db_if_needed(issueInfo, trackerURL, user)
            result["issueInfo"] = issueInfo.__dict__
    return result

def _append_project_id_and_update_db_if_needed(issueInfo, trackerURL, user):
    issueInfo.project_id = ''
    project = None
    if(issueInfo.project_trackerURL):
        found_projects = Project.objects.filter(trackerURL__iexact=issueInfo.project_trackerURL)
        if(found_projects.count() > 1):
            notify_admin("WARNING: Database inconsistency", "more than one project found with url = %s"%issueInfo.project_trackerURL)
        elif(found_projects.count() == 1):
            project = found_projects[0]
            _update_project_name_if_needed(project, issueInfo.project_name)
        else:
            project = _create_project(issueInfo, user)
    if(project):
        issueInfo.project_id = project.id
        issueInfo.project_homeURL = project.homeURL

def _update_project_name_if_needed(project, project_name):
    if(project.name != project_name):
        project.name = project_name
        project.save()

def _create_project(issueInfo, createdByUser):
    project = Project.newProject(issueInfo.project_name, createdByUser, '', issueInfo.project_trackerURL)
    project.save()
    notify_admin("INFO: Project created from json view", "issue key: "+issueInfo.key+"\n<br>"+ \
        "issue key: "+issueInfo.key+"\n<br>"+ \
        "project : "+project.name+"\n<br>"+ \
        "project.trackerURL: "+project.trackerURL+"\n<br>")
    return project

