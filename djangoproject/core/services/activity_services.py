from core.models import ActionLog
from django.db.models import Q

__author__ = 'tony'


def get_latest_activity(project_id, offset):
    query = ActionLog.objects.all()
    if project_id:
        query = query.filter(Q(project__id=project_id) & (~Q(action__in=['ADD_ISSUE_COMMENT', 'EDIT_ISSUE_COMMENT'])))
    query = query.order_by('-creationDate')
    return query[offset: offset + 10], query.count()
