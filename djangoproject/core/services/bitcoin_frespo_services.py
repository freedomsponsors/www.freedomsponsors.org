__author__ = 'tony'
from core.models import *
from core.utils.frespo_utils import get_or_none
from core.services import mail_services, watch_services
from bitcoin_frespo.utils import bitcoin_adapter
import logging
from django.db.models import Q
import datetime
from django.utils import timezone
from bitcoin_frespo.services import bitcoin_services
from decimal import Decimal

logger = logging.getLogger(__name__)

def bitcoin_ipn_received(value, destination_address, transaction_hash, confirmations):
    receive_address = get_or_none(ReceiveAddress, address = destination_address)
    if receive_address:
        payment = Payment.objects.get(bitcoin_receive_address__id = receive_address.id)
        double_payment = payment.bitcoin_transaction_hash and payment.bitcoin_transaction_hash != transaction_hash
        if not double_payment:
            payment.confirm_bitcoin_ipn(value, transaction_hash)
            logger.info('IPN bitcoin receive confirmation for payment id=%s, issue=%s' %
                        (payment.id, payment.offer.issue.title))
        else :
            _notify_ipn_receive_double_payment(payment, transaction_hash, value)
    else:
        mail_services.notify_admin('Received bitcoins outside FS', 'address = %s,\n value = %s,\n hash = %s' % (destination_address, value, transaction_hash))

def bitcoin_ipn_sent(value, destination_address, transaction_hash, confirmations):
    part = get_or_none(PaymentPart, money_sent__transaction_hash = transaction_hash)
    if part:
        values_equal = Decimal(str(value)) == part.realprice
        if values_equal:
            part.money_sent.confirm_ipn()
        else:
            mail_services.notify_admin('Theres a difference between bitcoin sent values',
                                       'part id = %s,\n part realprice = %s,\n value sent = %s' % (part.id, part.realprice, value))
    else:
        mail_services.notify_admin('Sent bitcoins outside FS', 'address = %s,\n value = %s,\n hash = %s' % (destination_address, value, transaction_hash))

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
    payments = _filter_payments_pending_active_receive_confirmation()
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

def _filter_payments_pending_active_receive_confirmation():
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

def bitcoin_active_send_confirmation():
    parts = _filter_paymentparts_pending_send_confirmation()
    previous_payment_id = None
    current_payment_id = None
    for part in parts:
        current_payment_id = part.payment.id
        valid, verr = _validate_paymentpart_for_active_send_confirmation(part)
        if valid:
            trn = bitcoin_adapter.get_transaction(part.money_sent.transaction_hash)
            if trn.confirmations >= 3:
                match, merr = _match_transaction_with_money_sent(part.money_sent, trn)
                if match:
                    part.money_sent.confirm_trn()
                    finished_payment = previous_payment_id is not None and current_payment_id != previous_payment_id
                    if finished_payment:
                        _notify_payment_finished_if_applicable(previous_payment_id)
                else:
                    mail_services.notify_admin('Bitcoin transaction doesnt match money sent',
                        'partid = %s, \n merr = %s' % (part.id, merr))
        else:
            logger.error('invalid paymentpart for active send confirmation: %s / %s' % (part.id, verr))
        previous_payment_id = current_payment_id
    _notify_payment_finished_if_applicable(previous_payment_id)

def _notify_payment_finished_if_applicable(payment_id):
    payment = Payment.objects.get(pk = payment_id)
    parts = PaymentPart.objects.filter(payment__id = payment.id)
    is_finished = True
    for part in parts:
        if part.money_sent.status != MoneySent.CONFIRMED_TRN:
            is_finished = False
            break
    if is_finished:
        watches = watch_services.find_issue_and_offer_watches(payment.offer)
        mail_services.notify_payment_parties_and_watchers_paymentconfirmed(payment, watches)

def _filter_paymentparts_pending_send_confirmation():
    return PaymentPart.objects.filter(
        Q(money_sent__status = MoneySent.CONFIRMED_IPN)
        | (
            Q(money_sent__status = MoneySent.SENT)
            & Q(money_sent__lastChangeDate__lte=timezone.now() - datetime.timedelta(hours=1))
        )
    ).order_by('payment__id')

def _validate_paymentpart_for_active_send_confirmation(part):
    if not part.payment.currency == 'BTC':
        return False, 'Payment currency should be bitcoin'
    if not part.money_sent.status in [MoneySent.SENT, MoneySent.CONFIRMED_IPN]:
        return False, 'Invalid status %s' % part.money_sent.status
    return True, None

def _match_transaction_with_money_sent(money_sent, trn):
    trn_map = {}
    for detail in trn.details:
        key = detail['address']
        if not trn_map.has_key(key):
            trn_map[key] = detail['amount']
        else:
            trn_map[key] += detail['amount']
    if not trn_map.has_key(money_sent.from_address) or not trn_map.has_key(money_sent.to_address):
        return False, 'Adresses dont match'
    if not (money_sent.value == -trn_map[money_sent.from_address] and money_sent.value == trn_map[money_sent.to_address]):
        return False, 'Values dont match'
    return True, None

def bitcoin_pay_programmers():
    parts = _filter_paymentparts_pending_payment()
    for part in parts:
        valid, verr = _validate_paymentpart_for_send_money(part)
        if valid:
            part.money_sent = bitcoin_services.make_payment(from_address = part.payment.bitcoin_receive_address.address,
                to_address = part.solution.programmer.getUserInfo().bitcoin_receive_address,
                value = part.realprice)
            part.save()
            logger.info('MoneySent_%s %s bitcoins to programmer %s on address %s' %
                        (part.money_sent.id,
                         part.money_sent.value,
                         part.solution.programmer.getUserInfo().screenName,
                         part.money_sent.to_address))
        else:
            logger.error('invalid paymentpart sending money: %s / %s' % (part.id, verr))

def _filter_paymentparts_pending_payment():
    return PaymentPart.objects.filter(payment__currency = 'BTC', payment__status = Payment.CONFIRMED_TRN, money_sent = None)

def _validate_paymentpart_for_send_money(part):
    if part.money_sent:
        return False, "Part should not have MoneySent"
    if not part.payment.status == Payment.CONFIRMED_TRN:
        return False, "Part payment status should be CONFIRMED_TRN"
    if not part.payment.currency == 'BTC':
        return False, "Part payment currency should be BTC"
    return True, None
