from decimal import Decimal
from core.services.mail_services import notify_payment_parties_and_watchers_paymentconfirmed, notify_admin
from core.services import watch_services
from core.utils import paypal_adapter
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

def payment_confirmed_web(current_payment_id):
    curr_payment = Payment.objects.get(pk=int(current_payment_id))
    curr_payment.confirm_web()
    curr_payment.offer.paid()
    msg = 'Payment confirmed'
    return curr_payment, msg


def process_ipn_return(paykey, status, tracking_id):
    if(status == 'COMPLETED'):
        payment = get_or_none(Payment, paykey=paykey, confirm_key=tracking_id)
        if not payment:
            raise BaseException('payment not found ' + paykey)
        if payment.status == Payment.CONFIRMED_IPN:
            return #double notification, nothing to do
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

def accepts_paypal_payments(user):
    if user.getUserInfo().paypal_verified:
        return True
    _check_whether_user_has_verified_paypal(user)
    return user.getUserInfo().paypal_verified

def _check_whether_user_has_verified_paypal(user):
    userinfo = user.getUserInfo()
    userinfo.paypal_verified = paypal_adapter.is_verified_account(userinfo.paypalEmail)
    userinfo.save()