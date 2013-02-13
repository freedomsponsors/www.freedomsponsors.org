from django.test import TestCase
from django.utils.unittest import skipIf
from django.conf import settings

from bitcoin_frespo.utils import bitcoin_adapter

__author__ = 'tony'

@skipIf(settings.ENVIRONMENT != 'DEV', 'not supported in this environment')
class BitcoinAdapter(TestCase):
    def test_get_balance(self):
    	c = bitcoin_adapter._connect()
    	bal = c.getbalance()
    	print(bal)





