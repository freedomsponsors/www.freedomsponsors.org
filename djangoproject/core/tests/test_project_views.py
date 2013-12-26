from StringIO import StringIO

import mock
from django.test import TestCase
from helpers import test_data
from django.test.client import Client
from django.core.urlresolvers import reverse


__author__ = 'tony'


def _reverse(project_view, **kwargs):
    return reverse('core.views.project_views.' + project_view, kwargs=kwargs)


class TestProjectViews(TestCase):

    def setUp(self):
        self.project = test_data.create_dummy_project()
        self.client = Client()

    def test_project_list(self):
        response = self.client.get(_reverse('list'))
        self.assertTemplateUsed(response, 'core2/project_list.html')
        projects = response.context['projects']
        self.assertEqual('Hibernate', projects[0].name)

    def test_project_view(self):
        response = self.client.get(_reverse('view', project_id=self.project.id))
        self.assertTemplateUsed(response, 'core2/project.html')
        project = response.context['project']
        self.assertEqual('Hibernate', project.name)

    def test_project_edit_form(self):
        self.user = test_data.createDummyUserRandom(login='johndoe', password='abc123')
        self.client.login(username=self.user.username, password='abc123')
        self.client.login(username='johndoe', password='abc123')
        response = self.client.get(_reverse('edit_form', project_id=self.project.id))
        self.assertTemplateUsed(response, 'core2/project_edit.html')
        project = response.context['project']
        self.assertEqual('Hibernate', project.name)

    def test_project_edit(self):
        self.user = test_data.createDummyUserRandom(login='johndoe', password='abc123')
        self.client.login(username=self.user.username, password='abc123')
        file_obj = StringIO()
        setattr(file_obj, 'name', 'mock.jpg')
        with mock.patch.object(self.project, 'save') as _save:
            response = self.client.post(_reverse('edit'),
                                        {'id': self.project.id, 'image3x1': file_obj})
            self.assertTrue(_save.has_been_called())
        location = response._headers['location'][1]
        self.assertTrue(location.endswith(_reverse('view', project_id=self.project.id)))


class TestDeprecatedCoreProjectViews(TestCase):

    def setUp(self):
        self.client = Client()

    def assert_permanent_redirect(self, expected_url, deprecated_url, status_code=301):
        response = self.client.get(deprecated_url)
        self.assertEqual(response.status_code, status_code)
        location = response._headers['location'][1]
        self.assertTrue(location.endswith(expected_url))

    def test_project_list(self):
        self.assert_permanent_redirect(_reverse('list'), '/core/project/')

    def test_project_view(self):
        project = test_data.create_dummy_project()
        self.assert_permanent_redirect(_reverse('view', project_id=project.id),
            '/core/project/%s/' % project.id)

    def test_project_edit_form(self):
        project = test_data.create_dummy_project()
        self.assert_permanent_redirect(_reverse('edit_form', project_id=project.id),
            '/core/project/%s/edit' % project.id)
