from django.utils import unittest
from registration.forms import RegistrationForm
from django.test.client import Client

class TestRegistration(unittest.TestCase):

    def setUp(self):
        self.client = Client()

    def test_get(self):
        response = self.client.get('/accounts/register/')
        self.assertIsInstance(response.context['form'], RegistrationForm)
