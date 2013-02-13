from bitcoin_frespo.models import *

class BitcoinFrespoException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def get_available_receive_address():
    availables = ReceiveAddress.objects.filter(available = True)
    if availables.count() == 0:
        raise BitcoinFrespoException('No Bitcoin receive addresses available at this time. Try again in a few minutes')
    address = availables[0]
    address.use()
    return address
