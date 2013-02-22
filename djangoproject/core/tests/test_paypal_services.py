from core.models import *
from django.utils import unittest
from core.services import paypal_services, watch_services
from helpers import test_data, email_asserts
from django.conf import settings
from django.utils.unittest import skipIf
from paypalx import AdaptivePayments
from django.test.client import Client
from core.utils import paypal_adapter

__author__ = 'tony'

class TestPaypalPayment(unittest.TestCase):

    def test_paypal_payment_complete(self):

        #setup
        offer = test_data.create_dummy_offer_usd()
        programmer = test_data.create_dummy_programmer()
        programmer_userinfo = programmer.getUserInfo()
        programmer_userinfo.paypalEmail = test_data.paypal_credentials_1['email']
        programmer_userinfo.save()
        solution = Solution.newSolution(offer.issue, programmer, False)
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
        self.assertEqual(float(response_shared_price), 10.0)
        self.assertEqual(float(response_convert_rate), 1.0)
        self.assertEqual(response_currency_symbol, 'US$')

        #submit pay form
        response = client.post('/core/offer/pay/submit',
                               {'offer_id' : str(offer.id),
                                'count' : '1',
                                'check_0' : 'true',
                                'pay_0' : '10.00',
                                'solutionId_0' : str(solution.id)})
        self.assertEqual(response.status_code, 302)
        prefix = 'https://www.sandbox.paypal.com/webscr?cmd=_ap-payment&paykey='
        location = response.get('location')
        self.assertTrue(prefix in location)
        paykey = location.split(prefix)[1]
        self.assertTrue(paykey is not None)

        #RECEIVE ipn confirmation
        def mock_verify_ipn(data):
            return True

        paypal_adapter.verify_ipn = mock_verify_ipn

        payment = Payment.objects.get(paykey = paykey)
        client2 = Client()
        response = client2.post('/core/paypal/'+settings.PAYPAL_IPNNOTIFY_URL_TOKEN,
           {'pay_key' : paykey,
            'status' : 'COMPLETED',
            'tracking_id' : payment.confirm_key,})
            # 'tracking_id' : 'BLAU',})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, 'OK')
        payment = Payment.objects.get(pk = payment.id)
        self.assertEqual(payment.status, Payment.CONFIRMED_IPN)


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
        receivers = [{'amount' : '10.00', 'email' : receiver_email}]
        receivers = [{'amount' : '10.00', 'email' : 'receiver2@somewhere.com'},
                     {'amount' : '10.00', 'email' : 'receiver1@somewhere.com'}]
        response = paypal.pay(
            actionType = 'PAY',
            cancelUrl = settings.PAYPAL_CANCEL_URL,
            currencyCode = 'USD',
            # senderEmail = 'sender@somewhere.com', #no need to set this
            feesPayer = fees_payer,
            receiverList = { 'receiver': receivers },
            returnUrl = settings.PAYPAL_RETURN_URL,
            ipnNotificationUrl = settings.PAYPAL_IPNNOTIFY_URL
        )
        paykey = response['payKey']
        self.assertTrue(paykey is not None)

