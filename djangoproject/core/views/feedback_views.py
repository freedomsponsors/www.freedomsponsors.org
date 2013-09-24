from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from core.models import *
from django.shortcuts import render_to_response, redirect
from django.template import Context, loader, RequestContext
from core.services import watch_services
from core.services.mail_services import notify_admin
from core.views import template_folder


def feedback(request):
    issues = Issue.objects.filter(is_feedback=True).order_by('-creationDate')
    return render_to_response(template_folder(request) + 'feedback.html',
        {'issues':issues,},
        context_instance = RequestContext(request))

@login_required
def addFeedback(request):
    dict = request.POST
    issue_title = dict['title']
    issue_description = dict['description']
    if(not issue_title or not issue_description):
        raise BaseException(_('title and description are required'))
    issue = Issue.newIssueFeedback(issue_title, issue_description, request.user)
    issue.save()
    watch_services.watch_issue(request.user, issue.id, IssueWatch.CREATED)
    notify_admin(_('new Feedback: %s') % issue_title, issue_description)
    return redirect('/core/feedback')
