__author__ = 'tony'
from django.dispatch import Signal


project_edited = Signal(providing_args=["user", "project", "old_json"])
project_tag_added = Signal(providing_args=["user", "project_id", "tag_name"])
project_tag_removed = Signal(providing_args=["user", "project_id", "tag_name"])
