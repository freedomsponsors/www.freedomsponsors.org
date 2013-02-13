from core.models import *
from django.utils import unittest
from core.services import watch_services
from helpers import test_data
from django.test.client import Client

__author__ = 'tony'

class TestWatchService(unittest.TestCase):

    def test_watch_toggle_issue(self):
        issue = test_data.create_dummy_issue()
        user = issue.createdByUser

        self.assertTrue(not watch_services.is_watching_issue(user, issue.id))

        watch_services.watch_issue(user, issue.id, IssueWatch.WATCHED)
        self.assertTrue(watch_services.is_watching_issue(user, issue.id))

        watch_services.unwatch_issue(user, issue.id)
        self.assertTrue(not watch_services.is_watching_issue(user, issue.id))

    def test_watch_toggle_offer(self):
        offer = test_data.create_dummy_offer_usd()
        user = offer.issue.createdByUser

        self.assertTrue(not watch_services.is_watching_offer(user, offer.id))

        watch_services.watch_offer(user, offer.id, OfferWatch.WATCHED)
        self.assertTrue(watch_services.is_watching_offer(user, offer.id))

        watch_services.unwatch_offer(user, offer.id)
        self.assertTrue(not watch_services.is_watching_offer(user, offer.id))

