from django.http import HttpResponse
from core.utils.frespo_utils import dictOrEmpty
from bitcoin_frespo.services import bitcoin_services
from bitcoin_frespo.services.bitcoin_services import BitcoinFrespoException
from django.template import RequestContext
import logging
from django.contrib import messages
from django.shortcuts import redirect, render_to_response

logger = logging.getLogger(__name__)

def bitcoinIPN(request):
    logger.info('----- bitcoinIPN ------')
    logger.info("value: %s" % dictOrEmpty(request.GET, "value"))
    logger.info("input_address: %s" % dictOrEmpty(request.GET, "input_address"))
    logger.info("confirmations: %s" % dictOrEmpty(request.GET, "confirmations"))
    logger.info("transaction_hash: %s" % dictOrEmpty(request.GET, "transaction_hash"))
    logger.info("destination_address: %s" % dictOrEmpty(request.GET, "destination_address"))
    logger.info("input_transaction_hash: %s" % dictOrEmpty(request.GET, "input_transaction_hash"))
    logger.info("GET params: %s" % request.GET)
    logger.info('----- bitcoinIPN end ------')
    return HttpResponse("*ok*")

def payOffer(request, offer, payment):
    try:
        receive_address = bitcoin_services.get_available_receive_address()
        payment.bitcoin_receive_address = receive_address
        payment.save()
        return render_to_response('core/waitPaymentBitcoin.html',
            {'payment' : payment,
             'bitcoin_address' : receive_address.address,},
            context_instance = RequestContext(request))
    except BitcoinFrespoException as e:
        messages.error(request, e.value)
        return redirect(offer.get_view_link())



# non-anonymous
# 2013-02-04 23:59:31,170 [INFO] core.views.bitcoin_views: ----- bitcoinIPN ------
# 2013-02-04 23:59:31,171 [INFO] core.views.bitcoin_views: value: 1242290114
# 2013-02-04 23:59:31,171 [INFO] core.views.bitcoin_views: input_address: 
# 2013-02-04 23:59:31,172 [INFO] core.views.bitcoin_views: confirmations: 0
# 2013-02-04 23:59:31,172 [INFO] core.views.bitcoin_views: transaction_hash: 071118d0292762049de691e60efe5296987b1763710a4cf1eee938cd36087a57
# 2013-02-04 23:59:31,172 [INFO] core.views.bitcoin_views: destination_address: 1pjA3VSnEB6LKmJeJy9Jp1QY7vureFS4D
# 2013-02-04 23:59:31,173 [INFO] core.views.bitcoin_views: input_transaction_hash: 
# 2013-02-04 23:59:31,173 [INFO] core.views.bitcoin_views: GET params: <QueryDict: 
# {u'transaction_hash': [u'071118d0292762049de691e60efe5296987b1763710a4cf1eee938cd36087a57'], 
# u'value': [u'1242290114'], 
# u'confirmations': [u'0'], 
# u'anonymous': [u'false'], 
# u'address': [u'1pjA3VSnEB6LKmJeJy9Jp1QY7vureFS4D'], 
# u'test': [u'true'], 
# u'destination_address': [u'1pjA3VSnEB6LKmJeJy9Jp1QY7vureFS4D']}>
# 2013-02-04 23:59:31,173 [INFO] core.views.bitcoin_views: ----- bitcoinIPN end ------



# anonymous
# 2013-02-04 23:58:41,188 [INFO] core.views.bitcoin_views: ----- bitcoinIPN ------
# 2013-02-04 23:58:41,189 [INFO] core.views.bitcoin_views: value: 7129632005
# 2013-02-04 23:58:41,189 [INFO] core.views.bitcoin_views: input_address: 
# 2013-02-04 23:58:41,189 [INFO] core.views.bitcoin_views: confirmations: 0
# 2013-02-04 23:58:41,190 [INFO] core.views.bitcoin_views: transaction_hash: 25371aa8d93184a6f47a8f267be5a23feac8c396e6a39f40eb4cf3415cc16e08
# 2013-02-04 23:58:41,190 [INFO] core.views.bitcoin_views: destination_address: 1pjA3VSnEB6LKmJeJy9Jp1QY7vureFS4D
# 2013-02-04 23:58:41,190 [INFO] core.views.bitcoin_views: input_transaction_hash: 
# 2013-02-04 23:58:41,190 [INFO] core.views.bitcoin_views: GET params: <QueryDict: 
# {u'transaction_hash': [u'25371aa8d93184a6f47a8f267be5a23feac8c396e6a39f40eb4cf3415cc16e08'], 
# u'value': [u'7129632005'], 
# u'confirmations': [u'0'], 
# u'anonymous': [u'false'], 
# u'address': [u'1pjA3VSnEB6LKmJeJy9Jp1QY7vureFS4D'], 
# u'test': [u'true'], 
# u'destination_address': [u'1pjA3VSnEB6LKmJeJy9Jp1QY7vureFS4D']}>
# 2013-02-04 23:58:41,191 [INFO] core.views.bitcoin_views: ----- bitcoinIPN end ------


##send test:
#console:
# >>> c.sendfrom('12EiAPTUZN4LStdP9nP7K8ZBfhrm5Mg2RW', '1KExeHvN1PoCrA87xGTPHBR3DhEYFgDQV1',0.001)
# u'c406122df4a18fd1af51da3ef3c4e86fee84a47a249b86c28d2e316791a9c145'
# >>> c2.getbalance()
# Decimal('0.0')
# >>> c2.getreceivedbyaccount('1KExeHvN1PoCrA87xGTPHBR3DhEYFgDQV1')
# Decimal('0.0')
# >>> c2.getbalance()
# Decimal('0.001')
# >>> c2.getreceivedbyaccount('1KExeHvN1PoCrA87xGTPHBR3DhEYFgDQV1')
# Decimal('0.001')

# 2013-02-05 00:34:18,266 [INFO] core.views.bitcoin_views: ----- bitcoinIPN ------
# 2013-02-05 00:34:18,267 [INFO] core.views.bitcoin_views: value: -150000
# 2013-02-05 00:34:18,268 [INFO] core.views.bitcoin_views: input_address: 12EiAPTUZN4LStdP9nP7K8ZBfhrm5Mg2RW
# 2013-02-05 00:34:18,268 [INFO] core.views.bitcoin_views: confirmations: 2
# 2013-02-05 00:34:18,268 [INFO] core.views.bitcoin_views: transaction_hash: c406122df4a18fd1af51da3ef3c4e86fee84a47a249b86c28d2e316791a9c145
# 2013-02-05 00:34:18,269 [INFO] core.views.bitcoin_views: destination_address: 12EiAPTUZN4LStdP9nP7K8ZBfhrm5Mg2RW
# 2013-02-05 00:34:18,269 [INFO] core.views.bitcoin_views: input_transaction_hash: 
# 2013-02-05 00:34:18,269 [INFO] core.views.bitcoin_views: GET params: <QueryDict: {u'transaction_hash': [u'c406122df4a18fd1af51da3ef3c4e86fee84a47a249b86c28d2e316791a9c145'], u'value': [u'-150000'], u'confirmations': [u'2'], u'anonymous': [u'false'], u'address': [u'12EiAPTUZN4LStdP9nP7K8ZBfhrm5Mg2RW'], u'input_address': [u'12EiAPTUZN4LStdP9nP7K8ZBfhrm5Mg2RW'], u'destination_address': [u'12EiAPTUZN4LStdP9nP7K8ZBfhrm5Mg2RW']}>
# 2013-02-05 00:34:18,269 [INFO] core.views.bitcoin_views: ----- bitcoinIPN end ------

# 2013-02-05 00:37:15,252 [INFO] core.views.bitcoin_views: ----- bitcoinIPN ------
# 2013-02-05 00:37:15,252 [INFO] core.views.bitcoin_views: value: 100000
# 2013-02-05 00:37:15,253 [INFO] core.views.bitcoin_views: input_address: 1KExeHvN1PoCrA87xGTPHBR3DhEYFgDQV1
# 2013-02-05 00:37:15,253 [INFO] core.views.bitcoin_views: confirmations: 3
# 2013-02-05 00:37:15,253 [INFO] core.views.bitcoin_views: transaction_hash: c406122df4a18fd1af51da3ef3c4e86fee84a47a249b86c28d2e316791a9c145
# 2013-02-05 00:37:15,253 [INFO] core.views.bitcoin_views: destination_address: 1KExeHvN1PoCrA87xGTPHBR3DhEYFgDQV1
# 2013-02-05 00:37:15,254 [INFO] core.views.bitcoin_views: input_transaction_hash: 
# 2013-02-05 00:37:15,254 [INFO] core.views.bitcoin_views: GET params: <QueryDict: {u'transaction_hash': [u'c406122df4a18fd1af51da3ef3c4e86fee84a47a249b86c28d2e316791a9c145'], u'value': [u'100000'], u'confirmations': [u'3'], u'anonymous': [u'false'], u'address': [u'1KExeHvN1PoCrA87xGTPHBR3DhEYFgDQV1'], u'input_address': [u'1KExeHvN1PoCrA87xGTPHBR3DhEYFgDQV1'], u'destination_address': [u'1KExeHvN1PoCrA87xGTPHBR3DhEYFgDQV1']}>
# 2013-02-05 00:37:15,254 [INFO] core.views.bitcoin_views: ----- bitcoinIPN end ------