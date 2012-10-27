from core.models import *
from django.utils import unittest
from core.services import payment_services
from helpers import test_data, email_asserts

__author__ = 'tony'

class TestPaymentService(unittest.TestCase):

    def test_process_ipn_return(self):
        payment = test_data.create_dummy_payment()
        email_asserts.clear_sent()
        payment_services.process_ipn_return(payment.paykey, 'COMPLETED', 'abcd1234')
        payment = Payment.objects.get(id=payment.id);
        self.assertEquals(Payment.CONFIRMED_IPN, payment.status)
        email_asserts.send_emails()
        email_asserts.assert_sent_count(self, 2)
        email_asserts.assert_sent(self, to=payment.offer.sponsor.email, subject="You have made a US$ 10.00 payment")
        email_asserts.assert_sent(self, to=payment.getParts()[0].programmer.email, subject="User One has made you a US$ 10.00 payment")

