from bitcoin_frespo.services import bitcoin_services
from django.core.management.base import NoArgsCommand
from optparse import make_option

class Command(NoArgsCommand):

    help = "Refills the bitcoin receive address pool up to a size of settings.BITCOIN_RECEIVE_ADDRESS_POOL_SIZE"

    option_list = NoArgsCommand.option_list + (
        make_option('--verbose', action='store_true'),
    )
    
    def handle_noargs(self, **options):
        bitcoin_services.refill_receive_address_pool()
