from core.models import *
from django.utils import unittest
from core.services import watch_services
from helpers import test_data

__author__ = 'tony'


class TestWatchService(unittest.TestCase):

    def test_watch_toggle_issue(self):
        issue = test_data.create_dummy_issue()
        user = issue.createdByUser

        self.assertTrue(not watch_services.is_watching_issue(user, issue.id))

        watch_services.watch_issue(user, issue.id, Watch.WATCHED)
        self.assertTrue(watch_services.is_watching_issue(user, issue.id))

        watch_services.toggle_watch('ISSUE', issue.id, Watch.WATCHED)
        self.assertTrue(not watch_services.is_watching_issue(user, issue.id))
