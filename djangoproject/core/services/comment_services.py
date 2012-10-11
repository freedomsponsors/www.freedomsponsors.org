from core.services.mail_services import notifyWatchers_newoffercomment, notifyWatchers_newissuecomment
from core.models import Offer, OfferComment, IssueComment, Issue

__author__ = 'tony'

def add_comment_to_offer(offer_id, comment_content, user):
    offer = Offer.objects.get(pk=offer_id)
    comment = OfferComment.newComment(offer, user, comment_content)
    comment.save()
    notifyWatchers_newoffercomment(comment)
    return offer


def edit_comment_of_offer(comment_id, comment_content, user):
    comment = OfferComment.objects.get(pk=comment_id)
    _throwIfNotCommentAuthor(comment, user)
    comment.changeContent(comment_content)
    return comment


def edit_comment_of_issue(comment_id, comment_content, user):
    comment = IssueComment.objects.get(pk=comment_id)
    _throwIfNotCommentAuthor(comment, user)
    comment.changeContent(comment_content)
    return comment


def add_comment_to_issue(issue_id, comment_content, user):
    issue = Issue.objects.get(pk=issue_id)
    comment = IssueComment.newComment(issue, user, comment_content)
    comment.save()
    notifyWatchers_newissuecomment(comment)
    return issue

def _throwIfNotCommentAuthor(comment, user):
    if(not comment.author.id == user.id):
        raise BaseException('Security error. '+str(user.id)+' is not comment ('+str(comment.id)+') author. (Hey, if you do hack us, have the finesse to let us know, please - we are all firends here, right? ;-)')