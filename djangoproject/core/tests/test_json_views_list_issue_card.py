import json
from django.test import TestCase
from django.test.client import Client
from helpers import test_data

__author__ = 'cecile'


class TestData(TestCase):

    def setUp(self):
        self.client = Client()
        self.issue = test_data.create_dummy_issue()
     
    def test_list_issue_cards(self):
        response = self.client.get('/core/json/list_issue_cards?project_id=1&offset=0&count=3&sponsoring=false')
        self.assertEqual(response.status_code, 200)
        response_content = json.loads(response.content)
        self.assertEqual(response_content['count'], 1)
        self.assertEqual(response_content['issues'][0]['title'], 'Compiled native SQL queries are not cached')
        self.assertEqual(response_content['issues'][0]['id'], 1)
        self.assertEqual(response_content['issues'][0]['description'], 'meh')
        self.assertEqual(response_content['issues'][0]['sponsor_status'], 'PROPOSED')
