from bitcoin_frespo.services import bitcoin_services
from django.core.management.base import BaseCommand
from optparse import make_option
import traceback

class Command(BaseCommand):

    help = "Refills the bitcoin receive address pool up to a size of settings.BITCOIN_RECEIVE_ADDRESS_POOL_SIZE"

    def handle(self, *args, **kwargs):
        try:
            bitcoin_services.refill_receive_address_pool()
        except:
            traceback.print_exc()
