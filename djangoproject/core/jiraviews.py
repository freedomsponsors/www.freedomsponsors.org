from core.trackerutils import fetchIssueInfo
from core.models import *
from core.frespomail import notify_admin
from django.template import Context, loader, RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect

# TODO: separate URL /issue/add (sponsor new issue from inside FS) from issue/sponsor_jira (sponsor new issue from JIRA plugin's iframe)

# @login_required
# def sponsorJiraForm(request):
#     issue_trackerURL = request.GET['trackerURL']
#     issueInfo = fetchIssueInfo(issue_trackerURL)
#     issueInfo.project_id = ''
#     project = None


# def _update_project_name_if_needed(project, project_name):
#     if(project.name != project_name):
#         project.name = project_name
#         project.save()

# def _createProject(issueInfo, createdByUser):
#     project = Project.newProject(issueInfo.project_name, createdByUser, '', issueInfo.project_url)
#     project.save()
#     return project

