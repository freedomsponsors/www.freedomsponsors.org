__author__ = 'tony'
from core.models import *
from bitcoin_frespo.models import *
from core.utils.frespo_utils import get_or_none
from core.services import mail_services
from bitcoin_frespo.utils import bitcoin_adapter
import logging
from django.db.models import Q
import datetime
from django.utils import timezone

logger = logging.getLogger(__name__)

def bitcoin_ipn_received(value, destination_address, transaction_hash, confirmations):
    receive_address = get_or_none(ReceiveAddress, address = destination_address)
    if not receive_address:
        mail_services.notify_admin('Received bitcoins outside FS', 'address = %s, value = %s' % (destination_address, value))
    else:
        payment = Payment.objects.get(bitcoin_receive_address__id = receive_address.id)
        double_payment = payment.bitcoin_transaction_hash and payment.bitcoin_transaction_hash != transaction_hash
        if not double_payment:
            payment.confirm_bitcoin_ipn(value, transaction_hash)
        else :
            _notify_ipn_receive_double_payment(payment, transaction_hash, value)

def _notify_ipn_receive_double_payment(payment, transaction_hash, value):
        mail_services.notify_admin('bitcoin IPN RECEIVE double payment',
            """payment id: %s
old txn hash: %s
old value: %s
new txn hash: %s
new value: %s""" % (payment.id,
                    payment.bitcoin_transaction_hash,
                    payment.total_bitcoin_received,
                    transaction_hash,
                    value))

def bitcoin_active_receive_confirmation():
    payments = _filter_payments_pending_active_confirmation()
    for payment in payments:
        valid, verr = _validate_payment_for_active_receive_confirmation(payment)
        if valid:
            address = payment.bitcoin_receive_address.address
            amount_received = bitcoin_adapter.get_received_by_address(address)
            if amount_received > 0:
                payment.confirm_bitcoin_trn(amount_received)
                if payment.status == Payment.CONFIRMED_TRN:
                    logger.info('Actively Confirmed bitcoin full receive: %s/%s, addr: %s, payment_id: %s' %
                                (amount_received,
                                payment.total,
                                address,
                                payment.id))
                else:
                    logger.info('Actively Confirmed bitcoin underpay: %s/%s, addr: %s, payment_id: %s' %
                                (amount_received,
                                 payment.total,
                                 address,
                                 payment.id))
        else:
            logger.error('invalid payment for active receive confirmation: %s / %s' % (payment.id, verr))

def _filter_payments_pending_active_confirmation():
    return Payment.objects.filter(
        Q(currency='BTC')
        & (
            Q(status=Payment.CONFIRMED_IPN)
            | ( (Q(status=Payment.CREATED) | Q(status=Payment.CONFIRMED_IPN_UNDERPAY) | Q(status=Payment.CONFIRMED_TRN_UNDERPAY))
                & Q(lastChangeDate__gte=timezone.now() - datetime.timedelta(days=10))
                & Q(lastChangeDate__lte=timezone.now() - datetime.timedelta(hours=1))
              )
          )
    )

def _validate_payment_for_active_receive_confirmation(payment):
    if not payment.currency == 'BTC':
        return False, 'currency should be bitcoin'
    if not payment.status in [Payment.CONFIRMED_IPN, Payment.CREATED, Payment.CONFIRMED_IPN_UNDERPAY, Payment.CONFIRMED_TRN_UNDERPAY]:
        return False, 'invalid status: %s' % payment.status
    if payment.status in [Payment.CONFIRMED_TRN, Payment.CONFIRMED_TRN_UNDERPAY] and (not payment.bitcoin_transaction_hash or not payment.total_bitcoin_received):
        return False, 'expected a transaction hash and a total_bitcoin_value'
    return True, None