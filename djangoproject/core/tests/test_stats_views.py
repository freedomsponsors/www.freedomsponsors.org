from django.test import TestCase
from django.test.client import Client

__author__ = 'kang'

class TestStatsViews(TestCase):
    def setUp(self):
        self.client = Client()

    def test_stats_view(self):
        response = self.client.get('/stats/')
        self.assertTrue('Open offers amount to' in response.content)

