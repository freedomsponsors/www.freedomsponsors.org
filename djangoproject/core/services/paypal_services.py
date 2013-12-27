from core.services.mail_services import notify_payment_parties_and_watchers_paymentconfirmed, notify_admin
from core.services import watch_services, mail_services
from core.utils import paypal_adapter
from core.utils.frespo_utils import get_or_none, twoplaces
from core.models import Payment, ActionLog
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
    if status == 'COMPLETED':
        payment = get_or_none(Payment, paykey=paykey, confirm_key=tracking_id)
        if not payment:
            raise BaseException('payment not found ' + paykey)
        if payment.status == Payment.CONFIRMED_IPN:
            return  # double notification, nothing to do
        payment.confirm_ipn()
        payment.offer.paid()
        payment.offer.issue.touch()
        watches = watch_services.find_issue_watches(payment.offer.issue)
        notify_payment_parties_and_watchers_paymentconfirmed(payment, watches)
        notify_admin_payment_confirmed(payment)
        ActionLog.log_pay(payment)
    else:
        subject = 'received a payment confirmation with status = %s' % status
        msg = 'paykey = %s\nconfirm_key=%s' % (paykey, tracking_id)
        mail_services.notify_admin(subject, msg)
        logger.warn(subject)
        logger.warn(msg)


def notify_admin_payment_confirmed(payment):
    msg = 'payment confirmed: [%s %s / %s ]' % (
        payment.get_currency_symbol(),
        twoplaces(payment.total),
        payment.offer.issue.title
    )
    notify_admin(msg, payment.offer.get_view_link())


def accepts_paypal_payments(user):
    if user.getUserInfo().paypal_verified:
        return True
    _check_whether_user_has_verified_paypal(user)
    return user.getUserInfo().paypal_verified


def _check_whether_user_has_verified_paypal(user):
    userinfo = user.getUserInfo()
    userinfo.paypal_verified = paypal_adapter.is_verified_account(userinfo.paypalEmail)
    userinfo.save()