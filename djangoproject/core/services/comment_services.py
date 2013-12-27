from core.services.mail_services import notifyWatchers_newissuecomment
from core.models import IssueComment, Issue, ActionLog
from core.services import watch_services

__author__ = 'tony'


def edit_comment_of_issue(comment_id, comment_content, user):
    comment = IssueComment.objects.get(pk=comment_id)
    _throwIfNotCommentAuthor(comment, user)
    old_json = comment.to_json()
    comment.changeContent(comment_content)
    ActionLog.log_edit_issue_comment(issue_comment=comment, old_json=old_json)
    return comment


def add_comment_to_issue(issue_id, comment_content, user):
    issue = Issue.objects.get(pk=issue_id)
    issue.touch()
    comment = IssueComment.newComment(issue, user, comment_content)
    comment.save()
    watches = watch_services.find_issue_watches(comment.issue)
    notifyWatchers_newissuecomment(comment, watches)
    ActionLog.log_add_issue_comment(issue_comment=comment)
    return issue


def _throwIfNotCommentAuthor(comment, user):
    if not comment.author.id == user.id:
        raise BaseException('Security error. '+str(user.id)+' is not comment ('+str(comment.id)+') author. (Hey, if you do hack us, have the finesse to let us know, please - we are all firends here, right? ;-)')