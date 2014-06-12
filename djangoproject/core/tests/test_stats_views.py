from django.utils import unittest
from core.tests.helpers import test_data, email_asserts
from django.test.client import Client

__author__ = 'kang'

class TestStatsViews(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_stats_view(self):
        response = self.client.get('/core/stats/')
        self.assertTrue('Open offers amount to' in response.content)

