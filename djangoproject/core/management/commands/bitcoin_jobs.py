from django.core.management.base import BaseCommand
from optparse import make_option
from core.services import bitcoin_frespo_services, mail_services
import logging
import traceback

logger = logging.getLogger(__name__)


__author__ = 'tony'

class Command(BaseCommand):

    help = "Asynchronous Bitcoin transaction processing"

    def handle(*args, **options):
        try:
            bitcoin_frespo_services.bitcoin_active_receive_confirmation()
            bitcoin_frespo_services.bitcoin_pay_programmers()
            bitcoin_frespo_services.bitcoin_active_send_confirmation()
        except:
            logger.exception('Error running bitcoin jobs') #log configuration will ensure that admin e-mail is sent
            # mail_services.notify_admin('Error running bitcoin jobs', traceback.format_exc())
