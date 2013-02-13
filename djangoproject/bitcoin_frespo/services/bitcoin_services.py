from bitcoin_frespo.models import *
from django.conf import settings
from bitcoin_frespo.utils import bitcoin_adapter
import logging

logger = logging.getLogger(__name__)

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
    logger.info('Took bitcoin address from pool: [%s, %s]' % (address.id, address.address))
    return address

def refill_receive_address_pool():
    availables = ReceiveAddress.objects.filter(available = True)
    available_count = availables.count()
    new_count = settings.BITCOIN_RECEIVE_ADDRESS_POOL_SIZE - available_count
    for i in range(new_count):
        address = bitcoin_adapter.new_receive_address()
        address_entity = ReceiveAddress.newAddress(address)
        address_entity.save()
        logger.info('Added bitcoin address to pool: %s' % address)
