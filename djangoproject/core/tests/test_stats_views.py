from django.utils import unittest
from core.tests.helpers import test_data, email_asserts
from django.test.client import Client

__author__ = 'kang'


class TestStatsViews(unittest.TestCase):
    def setUp(self):
        self.user = test_data.createDummyUserRandom(login='johndoe', password='abc123')
        self.client = Client()
        self.client.login(username=self.user.username, password='abc123')

    def test_stats_view(self):
        response = self.client.get('/stats')
        self.assertTrue('Open offers amount to' in response.content)

