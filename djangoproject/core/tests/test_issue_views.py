#coding: utf-8
from unittest.case import skip
from django.contrib.auth.models import User
from django.test import TestCase
from helpers import test_data
from django.test.client import Client


class TestSearch(TestCase):
    def setUp(self):
        self.user = test_data.createDummyUserRandom(login='johndoe', password='abc123')
        self.client = Client()
        self.client.login(username=self.user.username, password='abc123')

    def test_search(self):
        project = test_data.create_dummy_project()
        test_data.create_dummy_issue(project, title='One')
        test_data.create_dummy_issue(project, title='Two')
        test_data.create_dummy_issue(project, title='Three')
        test_data.create_dummy_issue(project, title='Four')
        response = self.client.get('/search/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(4, len(response.context['issues']))
