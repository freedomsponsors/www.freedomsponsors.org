from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from core.services import comment_services

__author__ = 'tony'

@login_required
def addIssueComment(request):
    issue_id = int(request.POST['issue_id'])
    comment_content = request.POST['content']
    issue = comment_services.add_comment_to_issue(issue_id, comment_content, request.user)
    return redirect(issue.get_view_link())


@login_required
def addOfferComment(request):
    offer_id = int(request.POST['offer_id'])
    comment_content = request.POST['content']
    offer = comment_services.add_comment_to_offer(offer_id, comment_content, request.user)
    return redirect(offer.get_view_link())


@login_required
def editIssueComment(request):
    comment_id = int(request.POST['comment_id'])
    comment_content = request.POST['content']
    comment = comment_services.edit_comment_of_issue(comment_id, comment_content, request.user)
    return redirect(comment.issue.get_view_link())


@login_required
def editOfferComment(request):
    comment_id = int(request.POST['comment_id'])
    comment_content = request.POST['content']
    comment = comment_services.edit_comment_of_offer(comment_id, comment_content, request.user)
    return redirect(comment.offer.get_view_link())


