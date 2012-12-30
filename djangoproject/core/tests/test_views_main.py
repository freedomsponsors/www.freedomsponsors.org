# coding: utf-8
from django.test import TestCase


class HomeView(TestCase):
    def setUp(self):
        self.resp = self.client.get('/')

    def test_get(self):
        self.assertEquals(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'core/home.html')

    def test_context(self):
        self.assertIn('issues_sponsoring', self.resp.context)
        self.assertIn('issues_kickstarting', self.resp.context)

