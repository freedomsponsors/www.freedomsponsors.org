from django.core.management.base import NoArgsCommand
from optparse import make_option
from core.services import bitcoin_frespo_services

__author__ = 'tony'

class Command(NoArgsCommand):

    help = "Asynchronous Bitcoin transaction processing"

    option_list = NoArgsCommand.option_list + (
        make_option('--verbose', action='store_true'),
    )

    def handle_noargs(self, **options):
        bitcoin_frespo_services.bitcoin_active_receive_confirmation()
        bitcoin_frespo_services.bitcoin_pay_programmers()
