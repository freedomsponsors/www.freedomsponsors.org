from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from core.services.comment_services import add_comment_to_offer, edit_comment_of_offer, edit_comment_of_issue, add_comment_to_issue

__author__ = 'tony'

@login_required
def addIssueComment(request):
    issue_id = int(request.POST['issue_id'])
    comment_content = request.POST['content']
    issue = add_comment_to_issue(issue_id, comment_content, request.user)
    return redirect(issue.get_view_link())


@login_required
def addOfferComment(request):
    offer_id = int(request.POST['offer_id'])
    comment_content = request.POST['content']
    offer = add_comment_to_offer(offer_id, comment_content, request.user)
    return redirect(offer.get_view_link())


@login_required
def editIssueComment(request):
    comment_id = int(request.POST['comment_id'])
    comment_content = request.POST['content']
    comment = edit_comment_of_issue(comment_id, comment_content, request)
    return redirect(comment.issue.get_view_link())


@login_required
def editOfferComment(request):
    comment_id = int(request.POST['comment_id'])
    comment_content = request.POST['content']
    comment = edit_comment_of_offer(comment_id, comment_content, request)
    return redirect(comment.offer.get_view_link())


