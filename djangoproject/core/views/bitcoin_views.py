from django.http import HttpResponse
from core.utils.frespo_utils import dictOrEmpty

def bitcoinIPN(request):
    print('----- bitcoinIPN ------')
    print("value: %s" % dictOrEmpty(request.GET, "value"))
    print("input_address: %s" % dictOrEmpty(request.GET, "input_address"))
    print("confirmations: %s" % dictOrEmpty(request.GET, "confirmations"))
    print("transaction_hash: %s" % dictOrEmpty(request.GET, "transaction_hash"))
    print("destination_address: %s" % dictOrEmpty(request.GET, "destination_address"))
    print("input_transaction_hash: %s" % dictOrEmpty(request.GET, "input_transaction_hash"))
    return HttpResponse("*ok*")
