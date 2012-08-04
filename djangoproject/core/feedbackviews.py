from django.contrib.auth.decorators import login_required
from core.models import *
from django.conf import settings
from django.shortcuts import render_to_response, redirect
from django.template import Context, loader, RequestContext

def feedback(request):
    issues = Issue.objects.filter(project__id=settings.FRESPO_PROJECT_ID).order_by('-creationDate')
    return render_to_response('core/feedback.html',
        {'issues':issues,},
        context_instance = RequestContext(request))

@login_required
def addFeedback(request):
    frespo_project = Project.objects.get(pk=settings.FRESPO_PROJECT_ID)
    issue_title = request.POST['title']
    issue_description = request.POST['description']
    if(not issue_title or not issue_description):
        raise BaseException('title and description are required')
    issue = Issue.newIssue(frespo_project, '', issue_title, request.user, '')
    issue.description = issue_description
    issue.save()
    return redirect('/core/feedback')
