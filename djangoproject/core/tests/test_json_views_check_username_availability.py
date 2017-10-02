import json
from django.test import TestCase
from django.test.client import Client
from core.tests.helpers import test_data
from core.models import User

__author__ = 'cecile'


class TestData(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = 'Yummy'
        self.email = 'test@test.com'
        self.password = '12345'
        self.user = User.objects.create_user(self.username, self.email, self.password)
        self.logged_in = self.client.login(username=self.username, password=self.password)

        self.usernameExisted = "Existed"
        self.emailExisted = 'testExisted@test.com'
        self.passwordExisted = 'pwExisted'
        self.userExisted = User.objects.create_user(self.usernameExisted, self.emailExisted, self.passwordExisted)

    def test_check_username_availability_current(self):
        response_current = self.client.get('/core/json/check_username_availability/Yummy')
        self.assertEqual(response_current.status_code, 200)
        response_current_content = json.loads(response_current.content)
        self.assertEqual(response_current_content['ok'], False)
        self.assertEqual(response_current_content['message'], '"Yummy" is already your current username!')

    def test_check_username_availability_notValid(self):
        response_notValid = self.client.get('/core/json/check_username_availability/...')
        self.assertEqual(response_notValid.status_code, 200)
        response_notValid_content = json.loads(response_notValid.content)
        self.assertEqual(response_notValid_content['ok'], False)
        self.assertEqual(response_notValid_content['message'],
                         'Sorry! "..." is not a valid username (should be alphanumeric).')

    def test_check_username_availability_existed(self):
        response_existed = self.client.get('/core/json/check_username_availability/Existed')
        self.assertEqual(response_existed.status_code, 200)
        response_existed_content = json.loads(response_existed.content)
        self.assertEqual(response_existed_content['ok'], False)
        self.assertEqual(response_existed_content['message'], 'Sorry, "Existed" is already taken.')

    def test_check_username_availability_OK(self):
        response_OK = self.client.get('/core/json/check_username_availability/ABC')
        self.assertEqual(response_OK.status_code, 200)
        response_OK_content = json.loads(response_OK.content)
        self.assertEqual(response_OK_content['ok'], True)
        self.assertEqual(response_OK_content['message'], 'Great! "ABC" is available!')