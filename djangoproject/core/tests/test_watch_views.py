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

    def test_should_send_mail_when_watching_issue(self):
        offer = test_data.create_dummy_offer()
        issue = offer.issue
        response = self.client.get('/core/watch/issue/%s'%issue.id)
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/core/watch/offer/%s'%offer.id)
        self.assertEqual(response.status_code, 200)

        user2 = test_data.createDummyUserRandom(login='marydoe', password='xyz456')
        client2 = Client()
        client2.login(username=user2.username, password='xyz456')

        email_asserts.clear_sent()
        response = client2.post('/core/issue/comment/add/submit', {'issue_id': str(issue.id), 'content': 'Im adding a comment'})
        self.assertEqual(response.status_code, 302)

        email_asserts.send_emails()
        email_asserts.assert_sent_count(self, 1)
        email_asserts.assert_sent(self, to=self.user.email, subject="%s added a comment on issue [%s]"%(user2.getUserInfo().screenName, issue.title))

        email_asserts.clear_sent()
        response = client2.post('/core/offer/comment/add/submit', {'offer_id': str(offer.id), 'content': 'Im adding another comment'})
        self.assertEqual(response.status_code, 302)

        email_asserts.send_emails()
        email_asserts.assert_sent_count(self, 1)
        email_asserts.assert_sent(self, to=self.user.email, subject="%s added a comment on offer [US$ %s / %s]"%(user2.getUserInfo().screenName, '10.00', issue.title))
