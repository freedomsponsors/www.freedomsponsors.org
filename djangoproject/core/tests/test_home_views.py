from django.test import TestCase
from django.test.client import Client


class HomeViewsTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_redirect_core_home(self):
        response = self.client.get('/core/home/', follow=True)
        self.assertEqual([('/', 301)], response.redirect_chain)
