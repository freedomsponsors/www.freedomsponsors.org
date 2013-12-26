from core.models import ActionLog
from core.signals import project_edited, project_tag_added, project_tag_removed

__author__ = 'tony'
from django.dispatch import receiver


@receiver(project_edited)
def on_project_edited(sender, **kwargs):
    ActionLog.log_edit_project(kwargs['project'], kwargs['user'], kwargs['old_json'])


@receiver(project_tag_added)
def on_project_tag_added(sender, **kwargs):
    ActionLog.log_project_tag_added(kwargs['user'], kwargs['project_id'], kwargs['tag_name'])


@receiver(project_tag_removed)
def on_project_tag_removed(sender, **kwargs):
    ActionLog.log_project_tag_removed(kwargs['user'], kwargs['project_id'], kwargs['tag_name'])