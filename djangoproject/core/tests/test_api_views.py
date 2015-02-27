import json
from django.test import TestCase
from helpers import test_data
from django.test.client import Client
from core.models import Project

class TestGetProjectData(TestCase):
    def setUp(self):
        self.project = test_data.create_dummy_project()
        self.issue = test_data.create_dummy_issue(project=self.project)
        self.offer = test_data.create_dummy_offer_usd(issue=self.issue)
        self.issue.update_redundant_fields()
        self.client = Client()

    def test_get_project(self):
        response = self.client.get('/api/project/%s' % self.project.id)
        self.assertEqual(response.status_code, 200)
        project = json.loads(response.content)
        self.assertIsNotNone(project)
        self.assertEqual('Hibernate', project['name'])
        self.assertEqual(0.0, project['stats']['btc_open'])
        self.assertEqual(1, project['stats']['issues_open'])
        self.assertEqual(100, project['stats']['percent_issues_open'])
        self.assertEqual(10.0, project['stats']['usd_open'])


    def test_get_project_that_does_not_exist(self):
        responseNG = self.client.get('/api/project/10000000')
        self.assertEqual(responseNG.status_code, 404)
        projectNG = json.loads(responseNG.content)  		    
        self.assertEqual(projectNG['error'], 'Project not found')
