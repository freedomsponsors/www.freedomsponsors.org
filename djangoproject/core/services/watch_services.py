from core.models import *
from core.services.mail_services import *

__author__ = 'tony'


def find_issue_watches(issue):
    return Watch.objects.filter(entity='ISSUE', objid=issue.id)


def watch_issue(user, issue_id, reason):
    watch = _findWatchOrNone(user, 'ISSUE', issue_id)
    if not watch:
        issue = Issue.objects.get(pk=issue_id)
        watch = Watch.newWatch(user, 'ISSUE', issue.id, reason)
        watch.save()


def toggle_watch(user, entity, objid, reason):
    watch = _findWatchOrNone(user, entity, objid)
    if watch:
        watch.delete()
        return False
    else:
        watch = Watch.newWatch(user, entity, objid, reason)
        watch.save()
        return True


def is_watching_issue(user, issue_id):
    watch = _findWatchOrNone(user, 'ISSUE', issue_id)
    return not watch is None


def _findWatchOrNone(user, entity, objid):
    watches = Watch.objects.filter(user__id=user.id, entity=entity, objid=objid)
    count = len(watches)
    if count > 1:
        notify_admin("WARNING: Database inconsistency", "more than one Watch for user %s / %s %s" % (user.id, entity, objid))
    if count == 0:
        return None
    return watches[0]
