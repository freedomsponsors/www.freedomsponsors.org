from decimal import Decimal
from django.conf import settings
from core.services.mail_services import notify_payment_parties_and_watchers_paymentconfirmed, notify_admin
from core.services import watch_services
from core.utils.paypal_adapter import generate_paypal_payment
from core.utils.frespo_utils import get_or_none, twoplaces
from core.models import Payment, Offer, Solution, PaymentPart
from core.utils import google_calc_adapter
import logging

logger = logging.getLogger(__name__)

__author__ = 'tony'

def forget_payment(payment_id):
    curr_payment = Payment.objects.get(pk=payment_id)
    if(curr_payment.status != Payment.CONFIRMED_WEB and curr_payment.status != Payment.CONFIRMED_IPN):
        curr_payment.forget()


def generate_payment(offer_id, receiver_count, dict, user):
    offer = Offer.objects.get(pk=offer_id)
    if(offer.status == Offer.PAID):
        raise BaseException('offer %s is already paid' % offer.id + '. User %s' % user)
    payment = Payment.newPayment(offer)
    parts = []
    sum = Decimal(0)
    realSum = Decimal(0)
    for i in range(receiver_count):
        check = dict.has_key('check_%s' % i)
        if(check):
            pay = Decimal(dict['pay_%s' % i])
            if(pay > 0):
                solution = Solution.objects.get(pk=int(dict['solutionId_%s' % i]))
                realPay = Decimal(pay * Decimal(1 - settings.FS_FEE))
                part = PaymentPart.newPart(payment, solution.programmer, pay, realPay)
                parts.append(part)
                sum += pay
                realSum += realPay
    payment.fee = sum - realSum
    payment.total = sum
    payment.save()
    for part in parts:
        part.payment = payment
        part.save()
    generate_paypal_payment(payment)
    payment.save()
    return offer, payment


def payment_confirmed_web(current_payment_id):
    curr_payment = Payment.objects.get(pk=int(current_payment_id))
    curr_payment.confirm_web()
    curr_payment.offer.paid()
    msg = 'Payment confirmed'
    return curr_payment, msg


def process_ipn_return(paykey, status, tracking_id):
    if(status == 'COMPLETED'):
        payment = get_or_none(Payment, paykey=paykey, confirm_key=tracking_id)
        if(not payment):
            raise BaseException('payment not found ' + paykey)
        payment.confirm_ipn()
        payment.offer.paid()
        payment.offer.issue.touch()
        watches = watch_services.find_issue_and_offer_watches(payment.offer)
        notify_payment_parties_and_watchers_paymentconfirmed(payment, watches)
        notify_admin_payment_confirmed(payment)
    else:
        logger.warn('received a ' + status + ' IPN confirmation')

def notify_admin_payment_confirmed(payment):
    notify_admin('payment confirmed: [%s %s / %s]'%(payment.get_currency_symbol(), twoplaces(payment.total), payment.offer.issue.title),
        payment.offer.get_view_link())

def usd_2_brl_convert_rate():
    return google_calc_adapter.usd2brl() * 1.045

