from django.core.management.base import NoArgsCommand
from optparse import make_option
from core.services import bitcoin_frespo_services, mail_services
import logging
import traceback

logger = logging.getLogger(__name__)


__author__ = 'tony'

class Command(NoArgsCommand):

    help = "Asynchronous Bitcoin transaction processing"

    option_list = NoArgsCommand.option_list + (
        make_option('--verbose', action='store_true'),
    )

    def handle_noargs(self, **options):
        try:
            raise Exception('test')
            bitcoin_frespo_services.bitcoin_active_receive_confirmation()
            bitcoin_frespo_services.bitcoin_pay_programmers()
            bitcoin_frespo_services.bitcoin_active_send_confirmation()
        except:
            logger.exception('Error running bitcoin jobs')
            mail_services.notify_admin('Error running bitcoin jobs', traceback.format_exc())
