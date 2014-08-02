from django.test import TestCase
from registration.forms import RegistrationForm
from django.test.client import Client

class TestRegistration(TestCase):

    def setUp(self):
        self.client = Client()

    def test_get(self):
        response = self.client.get('/accounts/register/')
        self.assertIsInstance(response.context['form'], RegistrationForm)
