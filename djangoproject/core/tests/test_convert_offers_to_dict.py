from django.test import TestCase
from django.utils import timezone
from core.views.json_views import _convert_offers_to_dict
from helpers import test_data


class test_convert_offers_to_dict(TestCase):
    """ test for function _convert_offers_to_dict in core/views/json_views.py """
    
    def setUp(self):
        self.offer_usd = test_data.create_dummy_offer_usd()
        self.offer_btc = test_data.create_dummy_offer_btc()
    	
    def test_convert_offers_to_dict(self):
        result = _convert_offers_to_dict([self.offer_usd, self.offer_btc])

        self.assertEqual(result[0]['creationDate'][:19], str(timezone.now())[:19]) #compare up to seconds
        self.assertEqual(result[1]['creationDate'][:19], str(timezone.now())[:19])

        self.assertEqual(result[0]['lastChangeDate'][:19], str(timezone.now())[:19])
        self.assertEqual(result[1]['lastChangeDate'][:19], str(timezone.now())[:19])
        # didn't test for id, because it depends on how many dummy project/offer we created during the integration test
        self.assertEqual(result[0]['price'], '10.00')
        self.assertEqual(result[1]['price'], '5.00')

        self.assertEqual(result[0]['no_forking'], 'True')
        self.assertEqual(result[1]['no_forking'], 'True')

        self.assertEqual(result[0]['require_release'], 'True')
        self.assertEqual(result[1]['require_release'], 'True')

        self.assertEqual(result[0]['status'], 'OPEN')
        self.assertEqual(result[1]['status'], 'OPEN')
