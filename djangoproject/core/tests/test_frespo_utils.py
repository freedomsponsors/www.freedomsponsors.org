from django.test import TestCase
from django.utils import timezone
from datetime import timedelta, datetime
from core.utils.frespo_utils import strip_protocol, as_time_string

class TestFrespo_utils (TestCase):
	''' test for module core/utils/frespo_utils '''
	def setUp(self):
		self.url_input_1 = 'http://docs.oracle.com'
		self.url_input_2 = 'https://www.youtube.com'
		self.url_input_3 = 'facebook.com'
		self.date_input_1 = timezone.now() - timedelta(seconds = 4)
		self.date_input_2 = timezone.now() - timedelta(seconds = 50)
		self.date_input_3 = timezone.now() - timedelta(seconds = 3500)
		self.date_input_4 = timezone.now() - timedelta(hours = 20)
		self.date_input_5 = timezone.now() - timedelta(days = 20)
		self.date_input_6 = timezone.make_aware(datetime(2012, 12, 12), timezone.get_default_timezone())

	def test_strip_protocol(self):
		self.assertEqual(strip_protocol(self.url_input_1), 'docs.oracle.com')
		self.assertEqual(strip_protocol(self.url_input_2), 'www.youtube.com')
		self.assertEqual(strip_protocol(self.url_input_3), 'facebook.com')

	def test_as_time_string(self):
		self.assertEqual(as_time_string(self.date_input_1), 'just now')
		self.assertEqual(as_time_string(self.date_input_2), '50 seconds ago')
		self.assertEqual(as_time_string(self.date_input_3), '58 minutes ago')
		self.assertEqual(as_time_string(self.date_input_4), '20 hours ago')
		self.assertEqual(as_time_string(self.date_input_5), '20 days ago')
		self.assertEqual(as_time_string(self.date_input_6), 'on 2012/12/12')


