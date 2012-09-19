from core.frespomail import notifyProgrammers_newoffercomment, notifySponsors_newoffercomment, notifyProgrammers_newissuecomment, notifySponsors_newissuecomment
from core.models import Offer, OfferComment, IssueComment, Issue
from core.views.comment_views import _throwIfNotCommentAuthor

__author__ = 'tony'

def add_comment_to_offer(offer_id, comment_content, user):
    offer = Offer.objects.get(pk=offer_id)
    comment = OfferComment.newComment(offer, user, comment_content)
    comment.save()
    notifyProgrammers_newoffercomment(comment)
    notifySponsors_newoffercomment(comment)
    return offer


def edit_comment_of_offer(comment_id, comment_content, request):
    comment = OfferComment.objects.get(pk=comment_id)
    _throwIfNotCommentAuthor(comment, request.user)
    comment.changeContent(comment_content)
    return comment


def edit_comment_of_issue(comment_id, comment_content, request):
    comment = IssueComment.objects.get(pk=comment_id)
    _throwIfNotCommentAuthor(comment, request.user)
    comment.changeContent(comment_content)
    return comment


def add_comment_to_issue(issue_id, comment_content, user):
    issue = Issue.objects.get(pk=issue_id)
    comment = IssueComment.newComment(issue, user, comment_content)
    comment.save()
    notifyProgrammers_newissuecomment(comment)
    notifySponsors_newissuecomment(comment)
    return issue


def _throwIfNotCommentAuthor(comment, user):
    if(not comment.author.id == user.id):
        raise BaseException('Security error. '+str(user.id)+' is not comment ('+str(comment.id)+') author. (Hey, if you do hack us, have the finesse to let us know, please - we are all firends here, right? ;-)')