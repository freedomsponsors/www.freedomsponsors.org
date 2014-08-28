from django.contrib.auth.models import User
from django.core.management.base import NoArgsCommand
from optparse import make_option
import logging
from django.template.defaultfilters import slugify
from core.services import user_services

logger = logging.getLogger(__name__)


__author__ = 'tony'

class Command(NoArgsCommand):

    help = "Asynchronous Bitcoin transaction processing"

    option_list = NoArgsCommand.option_list + (
        make_option('--verbose', action='store_true'),
    )

    def handle_noargs(self, **options):
        count = 0
        for user in User.objects.all().order_by('id'):
            userinfo = user.getUserInfo()
            screenName = userinfo.screenName if userinfo else 'EMPTY'
            username = slugify(screenName)
            valid = user_services.is_valid_username(username)
            if userinfo:
                p = '[INVALID]' if not valid else ''
            else:
                p = '[NO_USERINFO]'
            if not valid:
                count += 1
            print('%s (%s) %s --> %s' % (p, user.id, screenName, username))
        print('----------------------------')
        print('invalid: %s' % count)
