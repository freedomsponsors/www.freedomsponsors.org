from django.conf import settings
from paypalx import AdaptivePayments, PaypalError
from urllib import urlencode
from urllib2 import urlopen, Request
from core.services import mail_services
import logging

logger = logging.getLogger(__name__)

paypal = AdaptivePayments(settings.PAYPAL_API_USERNAME, 
    settings.PAYPAL_API_PASSWORD, 
    settings.PAYPAL_API_SIGNATURE, 
    settings.PAYPAL_API_APPLICATION_ID, 
    settings.PAYPAL_API_EMAIL, 
    sandbox=settings.PAYPAL_USE_SANDBOX)
paypal.debug = settings.PAYPAL_DEBUG

if(settings.PAYPAL_USE_SANDBOX):
    WEBSCR_URL = 'https://www.sandbox.paypal.com/cgi-bin/webscr'
else:
    WEBSCR_URL = 'https://www.paypal.com/cgi-bin/webscr'

def generate_paypal_payment(payment):
    receivers = []
    for part in payment.getParts():
        receivers.append({'amount' : str(part.price), 'email' : part.programmer.getUserInfo().paypalEmail})
    receivers.append({'amount' : "%.2f"%payment.fee, 'email' : settings.PAYPAL_FRESPO_RECEIVER_EMAIL})
    response = paypal.pay(
        actionType= 'PAY',
        cancelUrl= settings.PAYPAL_CANCEL_URL,
        currencyCode= payment.currency,
#       senderEmail = offer.sponsor.getUserInfo().paypalEmail, //seems like we shouldn't use this
        feesPayer= 'SENDER',
        receiverList= { 'receiver': receivers},
        returnUrl= settings.PAYPAL_RETURN_URL,
        ipnNotificationUrl= settings.PAYPAL_IPNNOTIFY_URL,
        trackingId= str(payment.confirm_key)
    )
    logger.info('Paypal PAYREQUEST RECEIVERS=['+str(receivers)+'] / RESPONSE=['+str(response)+']')
    payment.setPaykey(response['payKey'])


def verify_ipn(data):
    # prepares provided data set to inform PayPal we wish to validate the response
    data["cmd"] = "_notify-validate"
    params = urlencode(data)
 
    # sends the data and request to the PayPal Sandbox
    req = Request(WEBSCR_URL, params)
    req.add_header("Content-type", "application/x-www-form-urlencoded")
    # reads the response back from PayPal
    response = urlopen(req)
    status = response.read()
    if status == "VERIFIED":
        logger.info('Paypal IPNVERIFY DATA=['+str(data)+'] / STATUS=['+status+']')
    else:
        logger.warn('Paypal IPNVERIFY DATA=['+str(data)+'] / STATUS=['+status+']')
    # If not verified
    if not status == "VERIFIED":
        return False

    return True

def is_verified_account(email):
    try:
        response = paypal.pay(
            actionType = 'PAY',
            cancelUrl = settings.PAYPAL_CANCEL_URL,
            currencyCode = 'USD',
            feesPayer = 'SENDER',
            receiverList = { 'receiver': { 'amount' : '10.00', 'email' : email } },
            returnUrl = settings.PAYPAL_RETURN_URL,
            ipnNotificationUrl = settings.PAYPAL_IPNNOTIFY_URL
        )
        return True
    except PaypalError as e:
        if e.code != '520009':
            msg = 'email:%s, error:%s' % (email, e)
            mail_services.notify_admin("Unexpected error from Paypal when trying to see if account exists", msg)
        return False
