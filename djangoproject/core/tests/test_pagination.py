from django.test import TestCase
from helpers import test_data
from django.test.client import Client
from django.http import HttpRequest
from core.templatetags.pagination import pagina
from django.template import Template, Context


class TestPagination(TestCase):
    def setUp(self):
        self.client = Client()
        self.request = HttpRequest()

    def testContextProjects(self):
        response = self.client.get('/project/')
        self.assertTemplateUsed(response, 'core2/project_list.html')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('projects' in response.context)
        self.assertContains(response, 'No projects found')

    def testPagina(self):
        list_number = []
        for i in range(33):
            list_number.append(i)
        projects = pagina(self.request, list_number)
        num_pages = 3
        self.assertEqual(num_pages, projects.paginator.num_pages)


class TestTemplateTag(TestCase):
    def setUp(self):
        self.list_projects = test_data.create_dummy_list_project()
        self.client = Client()
        self.request = HttpRequest()

    def testLoadPagination(self):
        projects = pagina(self.request, self.list_projects)
        t = Template("{% load pagination %} {% pagination projects %}")
        response = t.render(Context({'projects': projects, 'request': self.request}))
        self.assertTrue('<ul class="pagination">' in response)
        self.assertTrue('<li class="active" ><a href="?page=1">1</a></li>' in response)
        self.assertTrue('<li><a href="?page=2">2</a></li>' in response)
