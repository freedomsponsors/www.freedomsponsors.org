__author__ = 'tony'
from core.models import *
from bitcoin_frespo.models import *
from core.utils.frespo_utils import get_or_none
from core.services import mail_services
import logging

logger = logging.getLogger(__name__)

def bitcoin_ipn_received(value, destination_address, transaction_hash, confirmations):
    receive_address = get_or_none(ReceiveAddress, address = destination_address)
    if not receive_address:
        mail_services.notify_admin('Received bitcoins outside FS', 'address = %s, value = %s' % (destination_address, value))
    else:
        payment = Payment.objects.get(bitcoin_receive_address__id = receive_address.id)
        double_payment = payment.bitcoin_transaction_hash and payment.bitcoin_transaction_hash != transaction_hash
        if not double_payment:
            if payment.status == Payment.CREATED:
                if value >= payment.total:
                    payment.status = Payment.CONFIRMED_IPN
                else:
                    payment.status = Payment.CONFIRMED_IPN_UNDERPAY
                payment.total_bitcoin_received = value
            payment.bitcoin_transaction_hash = transaction_hash
            payment.save()
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
