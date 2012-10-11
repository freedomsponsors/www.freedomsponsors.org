from django.contrib.auth.decorators import login_required
from core.models import *
from django.shortcuts import render_to_response, redirect
from django.template import Context, loader, RequestContext
from core.services import watch_services

def feedback(request):
    issues = Issue.objects.filter(is_feedback=True).order_by('-creationDate')
    return render_to_response('core/feedback.html',
        {'issues':issues,},
        context_instance = RequestContext(request))

@login_required
def addFeedback(request):
    issue_title = dict['title']
    issue_description = dict['description']
    if(not issue_title or not issue_description):
        raise BaseException('title and description are required')
    issue = Issue.newIssueFeedback(issue_title, issue_description, request.user)
    issue.save()
    watch_services.watch_issue(request.user, issue.id, IssueWatch.CREATED)
    return redirect('/core/feedback')
