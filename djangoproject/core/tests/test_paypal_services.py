from core.models import *
from django.utils import unittest
from core.services import paypal_services, watch_services
from helpers import test_data, email_asserts
from django.conf import settings

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

