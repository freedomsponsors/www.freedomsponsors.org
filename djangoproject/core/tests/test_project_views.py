from StringIO import StringIO

import mock
from django.test import TestCase
from helpers import test_data
from django.test.client import Client


__author__ = 'tony'



class TestProjectViews(TestCase):

    def setUp(self):
        self.project = test_data.create_dummy_project()
        self.client = Client()

    def test_project_list(self):
        response = self.client.get('/project/')
        self.assertTemplateUsed(response, 'core2/project_list.html')
        projects = response.context['projects']
        self.assertEqual('Hibernate', projects[0].name)

    def test_project_view(self):
        response = self.client.get('/project/%s/' % self.project.id)
        self.assertTemplateUsed(response, 'core2/project.html')
        project = response.context['project']
        self.assertEqual('Hibernate', project.name)

    def test_project_edit_form(self):
        self.user = test_data.createDummyUserRandom(login='johndoe', password='abc123')
        self.client.login(username=self.user.username, password='abc123')
        self.client.login(username='johndoe', password='abc123')
        response = self.client.get('/project/%s/edit' % self.project.id)
        self.assertTemplateUsed(response, 'core2/project_edit.html')
        project = response.context['project']
        self.assertEqual('Hibernate', project.name)

    def test_project_edit(self):
        self.user = test_data.createDummyUserRandom(login='johndoe', password='abc123')
        self.client.login(username=self.user.username, password='abc123')
        file_obj = StringIO()
        setattr(file_obj, 'name', 'mock.jpg')
        with mock.patch.object(self.project, 'save') as _save:
            response = self.client.post('/project/submit',
                                        {'id': self.project.id, 'image3x1': file_obj})
            self.assertTrue(_save.has_been_called())
        location = response._headers['location'][1]
        self.assertTrue(location.endswith('/project/%s' % self.project.id))
