from django.test import TestCase
from core.tests.helpers import test_data, email_asserts, mockers
from bitcoin_frespo.utils import bitcoin_adapter
from django.utils.unittest import skipIf
from core.models import *
from django.test.client import Client
from core.services import bitcoin_frespo_services
from core.utils import paypal_adapter
from frespo_currencies import currency_service

__author__ = 'tony'

@skipIf(settings.SKIPTESTS_BITCOINADAPTER, 'not supported in this environment')
class BitcoinAdapterTest(TestCase):
    def test_get_balance(self):
        c = bitcoin_adapter._connect()
        bal = c.getbalance()
        print(bal)


class BitcoinPaymentTests(TestCase):

    def _create_test_data(self, usd_offer=False):
        if usd_offer:
            offer = test_data.create_dummy_offer_usd()
        else:
            offer = test_data.create_dummy_offer_btc()
        programmer = test_data.create_dummy_programmer()
        test_data.create_dummy_bitcoin_receive_address_available()
        solution = Solution.newSolution(offer.issue, programmer, False)
        programmer_userinfo = solution.programmer.getUserInfo()
        programmer_userinfo.bitcoin_receive_address = 'fake_receive_address_programmer'
        programmer_userinfo.save()
        solution.accepting_payments = True
        solution.save()
        return offer, programmer, solution

    def _request_payment_form(self, client, offer, expect_usd=False):

        def is_verified_account_mock(email):
            return True
        paypal_adapter.is_verified_account = is_verified_account_mock

        response = client.get('/offer/%s/pay' % offer.id)
        self.assertEqual(response.status_code, 200)
        response_offer = response.context['offer']
        response_solutions = json.loads(response.context['solutions_json'])
        response_currency_options = json.loads(response.context['currency_options_json'])
        self.assertEqual(offer.id, response_offer.id)
        self.assertEqual(len(response_solutions), 1)
        self.assertEqual(offer.price, response_offer.price)
        if expect_usd:
            self.assertEqual(response_currency_options[0]['currency'], 'USD')
            self.assertTrue(response_currency_options[0]['rate'] == 1.0)
            self.assertEqual(response_currency_options[1]['currency'], 'BTC')
            self.assertTrue(response_currency_options[1]['rate'] == 0.01)
        else:
            self.assertEqual(response_currency_options[0]['currency'], 'USD')
            self.assertTrue(response_currency_options[0]['rate'] == 100.0)
            self.assertEqual(response_currency_options[1]['currency'], 'BTC')
            self.assertEqual(response_currency_options[1]['rate'], 1.0)
        return response_offer, response_solutions

    def _submitPayForm(self, client, offer, solutions, pay, pay_email_admin):
        response = client.post('/offer/pay/submit',
                               {'offer_id': str(offer.id),
                                'count': '1',
                                'check_0': 'true',
                                'currency': 'BTC',
                                'pay_0': pay,
                                'solutionId_0': str(solutions[0]['id'])})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            'Please make a BTC <strong>%s</strong> transfer to the following bitcoin address' % pay_email_admin in response.content)
        self.assertTrue('dummy_bitcoin_address_fs' in response.content)

    def _ipn_confirmation_receive(self, transfer_value):
        client2 = Client()
        response = client2.get('/core/bitcoin/' + settings.BITCOIN_IPNNOTIFY_URL_TOKEN,
                               {'value': str(transfer_value * Decimal('1E8')),
                                'destination_address': 'dummy_bitcoin_address_fs',
                                'transaction_hash': 'dummy_txn_hash',
                                'confirmations': '3'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, '*ok*')
        payment = Payment.objects.get(bitcoin_receive_address__address='dummy_bitcoin_address_fs')
        self.assertEqual(payment.status, Payment.CONFIRMED_IPN)
        return payment

    def _confirm_received(self, payment, value):
        def get_received_by_address_mock(address):
            print('mock get received by address: %s' % address)
            return value

        bitcoin_adapter.get_received_by_address = get_received_by_address_mock
        bitcoin_frespo_services.bitcoin_active_receive_confirmation()
        payment = Payment.objects.get(pk=payment.id)
        self.assertEqual(payment.status, Payment.CONFIRMED_TRN)
        return payment

    def _pay_programmer(self, payment, value, email_value):
        #Pay programmer
        def make_payment_mock(from_address, to_address, value):
            print('mock send bitcoins: %s ---(%s)---> %s' % (from_address, value, to_address))
            return 'dummy_txn_hash_2'

        bitcoin_adapter.make_payment = make_payment_mock
        email_asserts.clear_sent()
        bitcoin_frespo_services.bitcoin_pay_programmers()
        part = PaymentPart.objects.get(payment__id=payment.id)
        self.assertTrue(part.money_sent is not None)
        self.assertEqual(part.money_sent.value, value)
        self.assertEqual(part.money_sent.status, MoneySent.SENT)
        self.assertEqual(part.money_sent.transaction_hash, 'dummy_txn_hash_2')
        email_asserts.assert_sent_count(self, 2)
        subject = 'BTC %s payment received, and forwarded to programmer. Wating confirmation.' % email_value
        email_asserts.assert_sent(self, to=payment.offer.sponsor.email, subject=subject)
        email_asserts.assert_sent(self, to=settings.ADMINS[0][1], subject='[ADMIN NOTIFY] %s' % subject)

    def _ipn_confirmation_send(self, payment, transfer_value):
        client2 = Client()
        response = client2.get('/core/bitcoin/' + settings.BITCOIN_IPNNOTIFY_URL_TOKEN,
                               {'value': str(transfer_value * Decimal('1E8')),
                                'destination_address': 'fake_receive_address_programmer',
                                'transaction_hash': 'dummy_txn_hash_2',
                                'confirmations': '3', })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, '*ok*')
        part = PaymentPart.objects.get(payment__id=payment.id)
        self.assertEqual(part.money_sent.status, MoneySent.CONFIRMED_IPN)

    def _confirm_sent(self, offer, programmer, transaction_value, email_value1, email_value2):
        def get_transaction_mock(hash):
            class X:
                pass

            txn = X()
            txn.confirmations = 3
            txn.details = []
            txn.details.append({
                'address': 'fake_receive_address_programmer',
                'amount': transaction_value
            })
            txn.details.append({
                'address': 'dummy_bitcoin_address_fs',
                'amount': -transaction_value
            })
            return txn

        bitcoin_adapter.get_transaction = get_transaction_mock
        email_asserts.clear_sent()
        bitcoin_frespo_services.bitcoin_active_send_confirmation()
        email_asserts.assert_sent_count(self, 3)
        email_asserts.assert_sent(self, to=programmer.email,
                                  subject='%s has made you a BTC %s payment' % (offer.sponsor.getUserInfo().screenName, email_value1))
        email_asserts.assert_sent(self, to=offer.sponsor.email, subject='You have made a BTC %s payment' % email_value1)
        email_asserts.assert_sent(self, to=settings.ADMINS[0][1], subject='Bitcoin payment made - %s' % email_value2)

    def setUp(self):
        self.get_rate_old = currency_service.get_rate
        mockers.mock_currency_service()

    def tearDown(self):
        currency_service.get_rate = self.get_rate_old

    def test_bitcoin_payment_complete(self):

        offer, programmer, solution = self._create_test_data()

        client = Client()
        client.login(username=offer.sponsor.username, password='abcdef')

        response_offer, response_solutions = self._request_payment_form(client, offer)
        self._submitPayForm(client, response_offer, response_solutions, '5.00', '5.1502')
        payment = self._ipn_confirmation_receive(Decimal('5.1505'))
        payment = self._confirm_received(payment, 5.1505)
        self._pay_programmer(payment, Decimal('5'), '5.15050000')
        self._ipn_confirmation_send(payment, -Decimal('5'))
        self._confirm_sent(offer, programmer, Decimal('5'), '5.00', '5.15050000')

    def test_bitcoin_payment_complete_offer_usd(self):

        offer, programmer, solution = self._create_test_data(usd_offer=True)

        client = Client()
        client.login(username=offer.sponsor.username, password='abcdef')

        response_offer, response_solutions = self._request_payment_form(client, offer, expect_usd=True)
        self._submitPayForm(client, response_offer, response_solutions, '0.10', '0.1032')
        payment = self._ipn_confirmation_receive(Decimal('0.1035'))
        payment = self._confirm_received(payment, 0.1035)
        self._pay_programmer(payment, Decimal('0.1'), '0.10350000')
        self._ipn_confirmation_send(payment, -Decimal('0.1'))
        self._confirm_sent(offer, programmer, Decimal('0.1'), '0.10', '0.10350000')
