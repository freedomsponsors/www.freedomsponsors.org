from django.http import HttpResponse
from core.utils.frespo_utils import dictOrEmpty
import logging

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


# non-anonymous
# 2013-02-04 19:19:37,803 [INFO] core.views.bitcoin_views: ----- bitcoinIPN ------
# 2013-02-04 19:19:37,804 [INFO] core.views.bitcoin_views: value: 9900000
# 2013-02-04 19:19:37,805 [INFO] core.views.bitcoin_views: input_address: 
# 2013-02-04 19:19:37,805 [INFO] core.views.bitcoin_views: confirmations: 0
# 2013-02-04 19:19:37,805 [INFO] core.views.bitcoin_views: transaction_hash: 27629fdcd1d87b3af77601763586ff5b47051be67981cfb34b269376b38f4464
# 2013-02-04 19:19:37,805 [INFO] core.views.bitcoin_views: destination_address: 1pjA3VSnEB6LKmJeJy9Jp1QY7vureFS4D
# 2013-02-04 19:19:37,806 [INFO] core.views.bitcoin_views: input_transaction_hash: 
# 2013-02-04 19:19:37,806 [INFO] core.views.bitcoin_views: ----- bitcoinIPN end ------


# anonymous
# 2013-02-04 19:20:57,027 [INFO] core.views.bitcoin_views: ----- bitcoinIPN ------
# 2013-02-04 19:20:57,028 [INFO] core.views.bitcoin_views: value: 100092400
# 2013-02-04 19:20:57,028 [INFO] core.views.bitcoin_views: input_address: 
# 2013-02-04 19:20:57,028 [INFO] core.views.bitcoin_views: confirmations: 0
# 2013-02-04 19:20:57,029 [INFO] core.views.bitcoin_views: transaction_hash: 87730f2aece8bcc8aa263386d2f8a1aa89dbd703f26bac2f5619cad9340aaba0
# 2013-02-04 19:20:57,029 [INFO] core.views.bitcoin_views: destination_address: 1pjA3VSnEB6LKmJeJy9Jp1QY7vureFS4D
# 2013-02-04 19:20:57,029 [INFO] core.views.bitcoin_views: input_transaction_hash: 
# 2013-02-04 19:20:57,029 [INFO] core.views.bitcoin_views: ----- bitcoinIPN end ------
