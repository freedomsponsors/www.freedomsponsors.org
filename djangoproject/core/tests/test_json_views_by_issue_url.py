import json
from django.test import TestCase
from django.test.client import Client
from helpers import test_data

__author__ = 'cecile'


class TestData(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = test_data.createDummyUserRandom('Yummy', '12345')
        self.issue = test_data.create_dummy_issue()

    def test_by_issue_url(self):
        self.client.login(username = self.user.username, password = self.user.password)
        response = self.client.get('/core/json/by_issue_url?trackerURL=https://hibernate.onjira.com/browse/HHH-1051')
        self.assertEqual(response.status_code, 200)
        response_content = json.loads(response.content)
        self.assertEqual(response_content["urlValidationError"], '')
        self.assertEqual(response_content["issueInfo"]["project_name"], 'Hibernate')
        self.assertEqual(response_content["issueInfo"]["issue_title"], "Compiled native SQL queries are not cached")
        self.assertEqual(response_content["issueInfo"]["project_homeURL"], "www.hibernate.org")

    def test_by_issue_url_not_exist(self):
        responseNG = self.client.get('/core/json/by_issue_url')
        self.assertEqual(responseNG.status_code, 404)
        self.assertEqual(responseNG.content, "Error: need trackerURL parameter.")
        