import json
from django.test import TestCase
from core.tests.helpers import test_data
from django.test.client import Client
from core.models import ActionLog

__author__ = 'cecile'

class TestData(TestCase):

    def setUp(self):
        self.client = Client()
        self.payment = test_data.create_dummy_payment_usd()
        self.ActionLog = ActionLog.log_pay(self.payment)

    def test_latest_activity(self):
        response = self.client.get('/core/json/latest_activity?project_id=1&offset=0')
        self.assertEqual(response.status_code, 200)
        response_content = json.loads(response.content)
        self.assertEqual(response_content['count'], 1)
        self.assertEqual(response_content['activities'][0]['entity'],'PAYMENT')
        
