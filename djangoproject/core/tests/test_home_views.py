from django.utils import unittest
from core.services import watch_services
from core.tests.helpers import test_data, email_asserts
from django.test.client import Client


class TestHomeViews(unittest.TestCase):
    def setUp(self):
        self.client = Client()

    def test_redirect_core_home(self):
        response = self.client.get('/core/home/', follow=True)
        self.assertEqual([('http://testserver/', 301)], response.redirect_chain)
