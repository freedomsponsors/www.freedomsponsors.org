import json
from django.test import TestCase
from django.test.client import Client
from helpers import test_data

__author__ = 'cecile'


class TestProjectData(TestCase):

    def setUp(self):
        self.client = Client()
        self.project = test_data.create_dummy_project()

    def test_project(self):
        response = self.client.get('/core/json/project?query=H')
        self.assertEqual(response.status_code, 200)
        response_content = json.loads(response.content)
        self.assertTrue({"id": self.project.id, "value": "Hibernate"} in response_content)

    def test_project_not_exist(self):
        responseNG = self.client.get('/core/json/project')
        self.assertEqual(responseNG.status_code, 404)
        self.assertEqual(responseNG.content, "Error: need query parameter.")
