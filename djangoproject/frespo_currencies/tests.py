from django.test import TestCase
from frespo_currencies import currency_service

__author__ = 'tony'


class CurrencyServiceTests(TestCase):
    def test_currency_service(self):
        r = currency_service.get_rate('USD', 'BRL')
        r = currency_service.get_rate('USD', 'BTC')
        r = currency_service.get_rate('BTC', 'USD')
        r = currency_service.get_rate('BTC', 'BRL')
        pass
