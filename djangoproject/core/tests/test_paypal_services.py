import json
from core.models import *
from django.utils import unittest
from core.tests.helpers import mockers
from frespo_currencies import currency_service
from helpers import test_data
from django.conf import settings
from django.utils.unittest import skipIf
from paypalx import AdaptivePayments
from django.test.client import Client
from core.utils import paypal_adapter

__author__ = 'tony'


def _mock_paypal_adapter():
    def mock_is_verified_account(email):
        return True
    paypal_adapter.is_verified_account = mock_is_verified_account


class TestPaypalPayment(unittest.TestCase):

    def _create_test_data(self, bitcoin_offer=False):
        #setup
        if bitcoin_offer:
            offer = test_data.create_dummy_offer_btc()
        else:
            offer = test_data.create_dummy_offer_usd()
        programmer = test_data.create_dummy_programmer()
        programmer_userinfo = programmer.getUserInfo()
        programmer_userinfo.paypalEmail = test_data.paypal_credentials_1['email']
        programmer_userinfo.save()
        solution = Solution.newSolution(offer.issue, programmer, False)
        solution.accepting_payments = True
        solution.save()
        return offer, solution

    def _request_payment_form(self, offer, expect_brl=False, expect_btc=False):
        client = Client()
        client.login(username=offer.sponsor.username, password='abcdef')
        response = client.get('/core/offer/%s/pay' % offer.id)
        if response.status_code != 200:
            print('ERROR - was expecting 200, got %s' % response.status_code)
            for message in list(response.context['messages']):
                print('message: %s' % message)
        self.assertEqual(response.status_code, 200)
        response_offer = response.context['offer']
        response_solutions = json.loads(response.context['solutions_json'])
        response_currency_options = json.loads(response.context['currency_options_json'])
        self.assertEqual(offer.id, response_offer.id)
        self.assertEqual(len(response_solutions), 1)
        self.assertEqual(response_offer.price, offer.price)
        if expect_brl and not expect_btc:
            self.assertEqual(response_currency_options[0]['currency'], 'BRL')
            self.assertTrue(response_currency_options[0]['rate'] == 2.0)
            self.assertEqual(response_currency_options[1]['currency'], 'BTC')
            self.assertTrue(response_currency_options[1]['rate'] == 0.01)
        elif expect_btc and not expect_brl:
            self.assertEqual(response_currency_options[0]['currency'], 'USD')
            self.assertTrue(response_currency_options[0]['rate'] == 100.0)
            self.assertEqual(response_currency_options[1]['currency'], 'BTC')
            self.assertTrue(response_currency_options[1]['rate'] == 1.0)
        elif expect_btc and expect_brl:
            self.assertEqual(response_currency_options[0]['currency'], 'BRL')
            self.assertTrue(response_currency_options[0]['rate'] == 200.0)
            self.assertEqual(response_currency_options[1]['currency'], 'BTC')
            self.assertTrue(response_currency_options[1]['rate'] == 1.0)
        else:
            self.assertEqual(response_currency_options[0]['currency'], 'USD')
            self.assertEqual(response_currency_options[0]['rate'], 1.0)
            self.assertEqual(response_currency_options[1]['currency'], 'BTC')
            self.assertTrue(response_currency_options[1]['rate'] == 0.01)
        return client

    def _submit_pay_form(self, client, offer, solution, currency, pay):
        response = client.post('/core/offer/pay/submit',
                               {'offer_id': str(offer.id),
                                'count': '1',
                                'currency': currency,
                                'pay_0': pay,
                                'solutionId_0': str(solution.id)})
        self.assertEqual(response.status_code, 302)
        prefix = 'https://www.sandbox.paypal.com/webscr?cmd=_ap-payment&paykey='
        location = response.get('location')
        if prefix not in location:
            print('ERROR - was expecting redirect to paypal, got %s' % location)
            for message in list(response.context['messages']):
                print('message: %s' % message)
        self.assertTrue(prefix in location)
        paykey = location.split(prefix)[1]
        self.assertTrue(paykey is not None)
        return paykey

    def _ipn_confirmation_receive(self, paykey):
        def mock_verify_ipn(data):
            return True

        paypal_adapter.verify_ipn = mock_verify_ipn
        payment = Payment.objects.get(paykey=paykey)
        client2 = Client()
        response = client2.post('/core/paypal/' + settings.PAYPAL_IPNNOTIFY_URL_TOKEN,
                                {'pay_key': paykey,
                                 'status': 'COMPLETED',
                                 'tracking_id': payment.confirm_key})
        # 'tracking_id' : 'BLAU',})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, 'OK')
        payment = Payment.objects.get(pk=payment.id)
        self.assertEqual(payment.status, Payment.CONFIRMED_IPN)

    def setUp(self):
        self.get_rate_old = currency_service.get_rate
        mockers.mock_currency_service()

    def tearDown(self):
        currency_service.get_rate = self.get_rate_old

    def test_paypal_payment_complete(self):
        offer, solution = self._create_test_data()
        client = self._request_payment_form(offer)
        paykey = self._submit_pay_form(client, offer, solution, 'USD', '10.00')
        self._ipn_confirmation_receive(paykey)

    def test_paypal_payment_complete_brazilian_sponsor(self):
        offer, solution = self._create_test_data()
        sponsorinfo = offer.sponsor.getUserInfo()
        sponsorinfo.brazilianPaypal = True
        sponsorinfo.save()
        client = self._request_payment_form(offer, expect_brl=True)
        paykey = self._submit_pay_form(client, offer, solution, 'BRL', '20.00')
        self._ipn_confirmation_receive(paykey)

    def test_paypal_payment_complete_bitcoin_offer(self):
        offer, solution = self._create_test_data(bitcoin_offer=True)
        client = self._request_payment_form(offer, expect_btc=True)
        paykey = self._submit_pay_form(client, offer, solution, 'USD', '500.00')
        self._ipn_confirmation_receive(paykey)

    def test_paypal_payment_complete_bitcoin_offer_brazilian_sponsor(self):
        offer, solution = self._create_test_data(bitcoin_offer=True)
        sponsorinfo = offer.sponsor.getUserInfo()
        sponsorinfo.brazilianPaypal = True
        sponsorinfo.save()
        client = self._request_payment_form(offer, expect_brl=True, expect_btc=True)
        paykey = self._submit_pay_form(client, offer, solution, 'BRL', '1000.00')
        self._ipn_confirmation_receive(paykey)


@skipIf(settings.ENVIRONMENT != 'DEV', 'not supported in this environment')
class TestPaypalAPI(unittest.TestCase):

    def test_with_feesPayer_SENDER(self):

        fees_payer = 'SENDER'           #A
        # fees_payer = 'EACHRECEIVER'       #B

        receiver_email = 'receiver@somewhere.com'           #C
        # receiver_email = 'spon1_1348457115_per@gmail.com'   #D
        # receiver_email = 'tonylampada@gmail.com'   #E

        paypal = AdaptivePayments(settings.PAYPAL_API_USERNAME,
                                  settings.PAYPAL_API_PASSWORD,
                                  settings.PAYPAL_API_SIGNATURE,
                                  settings.PAYPAL_API_APPLICATION_ID,
                                  settings.PAYPAL_API_EMAIL,
                                  sandbox=settings.PAYPAL_USE_SANDBOX)
        receivers = [{'amount': '10.00', 'email': receiver_email}]
        receivers = [{'amount': '10.00', 'email': 'receiver2@somewhere.com'},
                     {'amount': '10.00', 'email': 'receiver1@somewhere.com'}]
        response = paypal.pay(
            actionType='PAY',
            cancelUrl=settings.PAYPAL_CANCEL_URL,
            currencyCode='USD',
            # senderEmail = 'sender@somewhere.com', #no need to set this
            feesPayer=fees_payer,
            receiverList={ 'receiver': receivers },
            returnUrl=settings.PAYPAL_RETURN_URL,
            ipnNotificationUrl=settings.PAYPAL_IPNNOTIFY_URL
        )
        paykey = response['payKey']
        self.assertTrue(paykey is not None)

