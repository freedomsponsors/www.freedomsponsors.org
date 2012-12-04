from django.utils import unittest
from core.services import watch_services
from core.tests.helpers import test_data, email_asserts
from django.test.client import Client
from helpers import email_asserts

__author__ = 'tony'

class TestFeedbackViews(unittest.TestCase):
    def setUp(self):
        self.user = test_data.createDummyUserRandom(login='johndoe', password='abc123')
        self.client = Client()
        self.client.login(username=self.user.username, password='abc123')

    def test_add_feedback(self):
        data = {'title' : 'Do Something!', 'description' : 'Something good'}

        email_asserts.clear_sent()
        response = self.client.post('/core/feedback/submit', data = data)
        self.assertEqual(response.status_code, 302)
        email_asserts.send_emails()
        email_asserts.assert_sent_count(self, 1)

        response = self.client.get('/core/feedback')
        self.assertTrue('We care a lot about what you think' in response.content)
        self.assertTrue('Do Something!' in response.content)
