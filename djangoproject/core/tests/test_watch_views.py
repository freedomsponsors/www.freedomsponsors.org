from core.models import *
from django.utils import unittest
from core.services import watch_services
from helpers import test_data, email_asserts
from django.test.client import Client

__author__ = 'tony'

class TestWatchViews(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.user = test_data.createDummyUserRandom(login='johndoe', password='abc123')
        self.client = Client()
        self.client.login(username=self.user.username, password='abc123')

    def test_watch_unwatch_issue(self):
        issue = test_data.create_dummy_issue()
        self.assertTrue(not watch_services.is_watching_issue(self.user, issue.id))

        response = self.client.get('/core/watch/issue/%s'%issue.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, 'WATCHING')
        self.assertTrue(watch_services.is_watching_issue(self.user, issue.id))

        response = self.client.get('/core/unwatch/issue/%s'%issue.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, 'NOT_WATCHING')
        self.assertTrue(not watch_services.is_watching_issue(self.user, issue.id))

    def test_watch_unwatch_offer(self):
        offer = test_data.create_dummy_offer()
        self.assertTrue(not watch_services.is_watching_offer(self.user, offer.id))

        response = self.client.get('/core/watch/offer/%s'%offer.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, 'WATCHING')
        self.assertTrue(watch_services.is_watching_offer(self.user, offer.id))

        response = self.client.get('/core/unwatch/offer/%s'%offer.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, 'NOT_WATCHING')
        self.assertTrue(not watch_services.is_watching_offer(self.user, offer.id))

