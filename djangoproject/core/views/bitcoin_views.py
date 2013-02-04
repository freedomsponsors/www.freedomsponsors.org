from django.http import HttpResponse
from core.utils.frespo_utils import get_or_none

def bitcoinIPN(request):
    print('----- bitcoinIPN ------')
    print("value: %s" % get_or_none(request.GET, "value"))
    print("input_address: %s" % get_or_none(request.GET, "input_address"))
    print("confirmations: %s" % get_or_none(request.GET, "confirmations"))
    print("transaction_hash: %s" % get_or_none(request.GET, "transaction_hash"))
    print("destination_address: %s" % get_or_none(request.GET, "destination_address"))
    print("input_transaction_hash: %s" % get_or_none(request.GET, "input_transaction_hash"))
    return HttpResponse("*ok*")
