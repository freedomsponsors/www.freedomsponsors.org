from django.test import TestCase
from django.utils.unittest import skipIf
from django.conf import settings
from bitcoin_frespo.utils import bitcoin_adapter
from core.tests.helpers import test_data
from core.models import *
from django.test.client import Client
from django.conf import settings

__author__ = 'tony'

@skipIf(settings.ENVIRONMENT != 'DEV', 'not supported in this environment')
class BitcoinAdapterTest(TestCase):
    def test_get_balance(self):
        c = bitcoin_adapter._connect()
        bal = c.getbalance()
        print(bal)

class BitcoinReceiveTests(TestCase):

    def test_wait_bitcoin_payment(self):
        offer = test_data.create_dummy_offer_btc()
        programmer = test_data.create_dummy_programmer()
        test_data.create_dummy_bitcoin_receive_address_available()
        solution = Solution.newSolution(offer.issue, programmer, False)
        programmer_userinfo = solution.programmer.getUserInfo()
        programmer_userinfo.bitcoin_receive_address = 'fake_receive_address_programmer'
        programmer_userinfo.save()
        solution.accepting_payments = True
        solution.save()

        client = Client()
        client.login(username=offer.sponsor.username, password='abcdef')

        response = client.get('/core/offer/%s/pay' % offer.id)
        self.assertEqual(response.status_code, 200)
        response_offer = response.context['offer']
        response_solutions_accepting_payments = response.context['solutions_accepting_payments']
        response_shared_price = response.context['shared_price']
        response_convert_rate = response.context['convert_rate']
        response_currency_symbol = response.context['currency_symbol']
        self.assertEqual(offer.id, response_offer.id)
        self.assertEqual(len(response_solutions_accepting_payments), 1)
        self.assertEqual(float(response_shared_price), 5.0)
        self.assertEqual(float(response_convert_rate), 1.0)
        self.assertEqual(response_currency_symbol, 'BTC')

        response = client.post('/core/offer/pay/submit',
            {'offer_id' : str(offer.id),
             'count' : '1',
             'check_0' : 'true',
             'pay_0' : '5.00',
             'solutionId_0' : str(solution.id)})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Please make a BTC <strong>5.00</strong> transfer to the following bitcoin address' in response.content)
        self.assertTrue('dummy_bitcoin_address_fs' in response.content)

        client2 = Client()
        response = client2.get('/core/bitcoin/'+settings.BITCOIN_IPNNOTIFY_URL_TOKEN,
            {'value' : '500000000',
             'destination_address' : 'dummy_bitcoin_address_fs',
             'transaction_hash' : 'dummy_txn_hash',
             'confirmations' : '3',})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, '*ok*')
        payment = Payment.objects.get(bitcoin_receive_address__address = 'dummy_bitcoin_address_fs')
        self.assertEqual(payment.status, Payment.CONFIRMED_IPN)

