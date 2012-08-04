from django.core.management.base import NoArgsCommand
from optparse import make_option
from core.models import *
from django.contrib.auth.models import User

from django.conf import settings
from paypalx import AdaptivePayments

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


def generatePayment():
	receivers = []

	receivers.append({'amount' : '5.70', 'email' : 'meupitukinho@gmail.com'})
	#receivers.append({'amount' : "%.2f"%0.10, 'email' : settings.PAYPAL_API_EMAIL})
	receivers.append({'amount' : "%.2f"%0.30, 'email' : 'calleriinformatica@gmail.com'})
	
	response = paypal.pay(
	    actionType = 'PAY',
	    cancelUrl = settings.PAYPAL_CANCEL_URL,
	    # currencyCode = 'BRL',
	    clientDetails = {'partnerName' : 'ratibum'},
	    currencyCode = 'USD',
	    feesPayer = 'EACHRECEIVER',
	    receiverList = { 'receiver': receivers},
	    returnUrl = settings.PAYPAL_RETURN_URL,
	    ipnNotificationUrl = settings.PAYPAL_IPNNOTIFY_URL
	)
	print ('Paypal PAYREQUEST RECEIVERS=['+str(receivers)+'] / RESPONSE=['+str(response)+']')
	paykey = response['payKey']
	print ('-------------------')
	print(WEBSCR_URL+'?cmd=_ap-payment&paykey='+paykey)



class Command(NoArgsCommand):

    help = "teste paypal"

    option_list = NoArgsCommand.option_list + (
        make_option('--verbose', action='store_true'),
    )
    
    def handle_noargs(self, **options):
        generatePayment()
