# coding: utf-8
from django.test import TestCase


class StatsView(TestCase):
    def setUp(self):
        self.resp = self.client.get('/core/stats/')

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'core/stats.html')

    def test_context(self):
        self.assertIn('stats', self.resp.context)

