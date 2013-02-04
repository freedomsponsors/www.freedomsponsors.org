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
    logger.info('----- bitcoinIPN end ------')
    return HttpResponse("*ok*")
