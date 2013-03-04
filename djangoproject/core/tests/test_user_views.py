from django.utils import unittest
from helpers import test_data
from django.test.client import Client


class TestRedirectToUser(unittest.TestCase):
    def setUp(self):
        self.user = test_data.createDummyUserRandom(login='johndoe', password='abc123')
        self.client = Client()
        self.client.login(username=self.user.username, password='abc123')

    def test_redirect_after_email_activation(self):
        response = self.client.get('/email/')
        self.assertEqual(response.status_code, 302)
        location = response['Location']
        self.assertIn(self.user.get_view_link(), location)
        self.assertIn('email_verified=true', location)
