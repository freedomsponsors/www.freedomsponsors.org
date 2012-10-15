from django.core.management.base import NoArgsCommand
from optparse import make_option
from gh_frespo_integration.services import github_services

class Command(NoArgsCommand):

    help = "Visita os issue trackers do github e deixa os comentarios de sponsorthis"

    option_list = NoArgsCommand.option_list + (
        make_option('--verbose', action='store_true'),
        )

    def handle_noargs(self, **options):
        github_services.add_sponsorthis_comments()