import json
from django.test import TestCase
from django.test.client import Client
from helpers import test_data

__author__ = 'cecile'

class TestData(TestCase):

    def setUp(self):
        self.client = Client()
        self.issue = test_data.create_dummy_issue()

    def test_by_issue_url(self):
        response = self.client.get('/core/json/by_issue_url?trackerURL=https://hibernate.onjira.com/browse/HHH-1051')
        self.assertEqual(response.status_code, 200)
        response_content = json.loads(response.content)
        self.assertEqual(response_content['urlValidationError'], '')
        self.assertEqual(response_content['issue']['id'], 1)

    def test_by_issue_url_NG(self):
        responseNG = self.client.get('/core/json/by_issue_url')
        self.assertEqual(responseNG.status_code, 404)
        self.assertEqual(responseNG.content, 'Error: need trackerURL parameter.')
