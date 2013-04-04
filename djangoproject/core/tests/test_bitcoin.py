from django.test import TestCase
from django.utils.unittest import skipIf
from django.conf import settings
from bitcoin_frespo.utils import bitcoin_adapter
from core.tests.helpers import test_data, email_asserts
from core.models import *
from django.test.client import Client
from core.services import bitcoin_frespo_services

__author__ = 'tony'

@skipIf(settings.ENVIRONMENT != 'DEV', 'not supported in this environment')
class BitcoinAdapterTest(TestCase):
    def test_get_balance(self):
        c = bitcoin_adapter._connect()
        bal = c.getbalance()
        print(bal)

class BitcoinPaymentTests(TestCase):

    def test_bitcoin_payment_complete(self):

        #setup
        offer = test_data.create_dummy_offer_btc()
        programmer = test_data.create_dummy_programmer()
        test_data.create_dummy_bitcoin_receive_address_available()
        solution = Solution.newSolution(offer.issue, programmer, False)
        programmer_userinfo = solution.programmer.getUserInfo()
        programmer_userinfo.bitcoin_receive_address = 'fake_receive_address_programmer'
        programmer_userinfo.save()
        solution.accepting_payments = True
        solution.save()

        #get pay form
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

        #submit pay form
        response = client.post('/core/offer/pay/submit',
            {'offer_id' : str(offer.id),
             'count' : '1',
             'check_0' : 'true',
             'pay_0' : '5.00',
             'solutionId_0' : str(solution.id)})
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Please make a BTC <strong>5.1500</strong> transfer to the following bitcoin address' in response.content)
        self.assertTrue('dummy_bitcoin_address_fs' in response.content)

        #RECEIVE ipn confirmation
        client2 = Client()
        response = client2.get('/core/bitcoin/'+settings.BITCOIN_IPNNOTIFY_URL_TOKEN,
            {'value' : '515000000',
             'destination_address' : 'dummy_bitcoin_address_fs',
             'transaction_hash' : 'dummy_txn_hash',
             'confirmations' : '3',})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, '*ok*')
        payment = Payment.objects.get(bitcoin_receive_address__address = 'dummy_bitcoin_address_fs')
        self.assertEqual(payment.status, Payment.CONFIRMED_IPN)

        #active RECEIVE confirmation
        def get_received_by_address_mock(address):
            print('mock get received by address: %s' % address)
            return 5.15

        bitcoin_adapter.get_received_by_address = get_received_by_address_mock
        bitcoin_frespo_services.bitcoin_active_receive_confirmation()

        payment = Payment.objects.get(pk = payment.id)
        self.assertEqual(payment.status, Payment.CONFIRMED_TRN)

        #Pay programmer
        def make_payment_mock(from_address, to_address, value):
            print('mock send bitcoins: %s ---(%s)---> %s' % (from_address, value, to_address))
            return 'dummy_txn_hash_2'

        bitcoin_adapter.make_payment = make_payment_mock
        bitcoin_frespo_services.bitcoin_pay_programmers()
        part = PaymentPart.objects.get(payment__id = payment.id)
        self.assertTrue(part.money_sent is not None)
        self.assertEqual(part.money_sent.value, Decimal('5'))
        self.assertEqual(part.money_sent.status, MoneySent.SENT)
        self.assertEqual(part.money_sent.transaction_hash, 'dummy_txn_hash_2')

        #SEND ipn confirmation
        response = client2.get('/core/bitcoin/'+settings.BITCOIN_IPNNOTIFY_URL_TOKEN,
                               {'value' : '-500000000',
                                'destination_address' : 'fake_receive_address_programmer',
                                'transaction_hash' : 'dummy_txn_hash_2',
                                'confirmations' : '3',})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, '*ok*')
        part = PaymentPart.objects.get(payment__id = payment.id)
        self.assertEqual(part.money_sent.status, MoneySent.CONFIRMED_IPN)

        def get_transaction_mock(hash):
            class X:
                pass

            txn = X()
            txn.confirmations = 3
            txn.details = []
            txn.details.append({
                'address':'fake_receive_address_programmer',
                'amount' : Decimal('5')
            })
            txn.details.append({
                'address':'dummy_bitcoin_address_fs',
                'amount' : Decimal('-5')
            })
            return txn

        bitcoin_adapter.get_transaction = get_transaction_mock
        bitcoin_frespo_services.bitcoin_active_send_confirmation()
        email_asserts.assert_sent_count(self, 3)
        email_asserts.assert_sent(self, to=programmer.email, subject='%s has made you a BTC 5.00 payment' % offer.sponsor.getUserInfo().screenName)
        email_asserts.assert_sent(self, to=offer.sponsor.email, subject='You have made a BTC 5.00 payment')
        email_asserts.assert_sent(self, to=settings.ADMINS[0][1], subject='Bitcoin payment made - 5.15')


