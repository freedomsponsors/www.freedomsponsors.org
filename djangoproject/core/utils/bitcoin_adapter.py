import bitcoinrpc
from django.conf import settings

def _connect():
	if(settings.BITCOINRPC_CONN['remote']):
		user = settings.BITCOINRPC_CONN['user']
		password = settings.BITCOINRPC_CONN['password']
		host = settings.BITCOINRPC_CONN['host']
		port = settings.BITCOINRPC_CONN['port']
		use_https = settings.BITCOINRPC_CONN['use_https']
		return bitcoinrpc.connect_to_remote(user=user, password=password, host=host, port=port, use_https=use_https)
	else:
		return bitcoinrpc.connect_to_local()
