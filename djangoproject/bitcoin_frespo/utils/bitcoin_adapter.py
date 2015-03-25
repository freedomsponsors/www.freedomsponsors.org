import bitcoinrpc
from django.conf import settings


def _connect():
    "Returns a new connection to the bitcoin daemon"
    if settings.BITCOINRPC_CONN['remote']:
        user = settings.BITCOINRPC_CONN['user']
        password = settings.BITCOINRPC_CONN['password']
        host = settings.BITCOINRPC_CONN['host']
        port = settings.BITCOINRPC_CONN['port']
        use_https = settings.BITCOINRPC_CONN['use_https']
        return bitcoinrpc.connect_to_remote(user=user, password=password, host=host, port=port, use_https=use_https)
    else:
        return bitcoinrpc.connect_to_local()


def new_receive_address():
    "Returns a String with the new receiving address"
    c = _connect()
    c.walletpassphrase(settings.BITCOINRPC_CONN['password2'], 4)
    return c.getnewaddress()


def get_received_by_address(address):
    "Returns a decimal with how much money was received by the given address"
    c = _connect()
    return float(c.getreceivedbyaccount(address))


def make_payment(from_address, to_address, value):
    c = _connect()
    c.walletpassphrase(settings.BITCOINRPC_CONN['password2'], 4)
    return c.sendfrom(from_address, to_address, value)


def get_transaction(hash):
    c = _connect()
    return c.gettransaction(hash)
