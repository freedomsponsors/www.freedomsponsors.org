from core.models import *
from django.utils import unittest
from core.services import paypal_services, watch_services
from helpers import test_data, email_asserts
from django.conf import settings
from django.utils.unittest import skipIf
from paypalx import AdaptivePayments

__author__ = 'tony'

class TestPaypalService(unittest.TestCase):

    def test_process_ipn_return(self):
        payment = test_data.create_dummy_payment_usd()
        watcher = test_data.create_dummy_programmer()
        watch_services.watch_issue(watcher, payment.offer.issue.id, IssueWatch.WATCHED)
        email_asserts.clear_sent()
        paypal_services.process_ipn_return(payment.paykey, 'COMPLETED', 'abcd1234')
        payment = Payment.objects.get(id=payment.id);
        self.assertEquals(Payment.CONFIRMED_IPN, payment.status)
        email_asserts.send_emails()
        email_asserts.assert_sent_count(self, 4)
        email_asserts.assert_sent(self, to=payment.offer.sponsor.email, subject="You have made a US$ 10.00 payment")
        email_asserts.assert_sent(self, to=payment.getParts()[0].programmer.email, subject="User One has made you a US$ 10.00 payment")
        email_asserts.assert_sent(self, to=watcher.email, subject="User One has paid his offer [US$ 10.00 / Compiled native SQL queries are not cached]")
        email_asserts.assert_sent(self, to=settings.ADMINS[0][1], subject="payment confirmed: [US$ 10.00 / Compiled native SQL queries are not cached]")

@skipIf(settings.ENVIRONMENT != 'DEV', 'not supported in this environment')
class TestPaypalAPI(unittest.TestCase):

    def test_x(self):

        fees_payer = 'SENDER'           #A
        # fees_payer = 'EACHRECEIVER'       #B

        # receiver_email = 'receiver@somewhere.com'           #C
        # receiver_email = 'spon1_1348457115_per@gmail.com'   #D
        receiver_email = 'tonylampada@gmail.com'   #E


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

