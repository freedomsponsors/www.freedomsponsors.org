from django.http import HttpResponse

def bitcoinIPN(request):
    print('----- bitcoinIPN ------')
    print("value: %s" % request.GET["value"])
    print("input_address: %s" % request.GET["input_address"])
    print("confirmations: %s" % request.GET["confirmations"])
    print("transaction_hash: %s" % request.GET["transaction_hash"])
    print("destination_address: %s" % request.GET["destination_address"])
    print("input_transaction_hash: %s" % request.GET["input_transaction_hash"])
    return HttpResponse("*ok*")
