from django.contrib.auth.models import User
from django.core.management.base import NoArgsCommand
from optparse import make_option
from django.template.defaultfilters import slugify
from core.services import user_services, mail_services


def _has_password(user):
    return user.password and len(user.password) > 1


def _user_with_password(user):
    subject = 'Important information about your account on FreedomSponsors'
    body = "TODO..."
    mail_services.plain_send_mail(user.email, subject, body)


def _user_with_same_screenName_already(user):
    pass


def _user_with_invalid_screenName(user):
    pass


def _user_default(user):
    pass


class Command(NoArgsCommand):

    help = "Copy screenName to username - one time deal"

    option_list = NoArgsCommand.option_list + (
        make_option('--verbose', action='store_true'),
    )

    def handle_noargs(self, **options):
        for user in User.objects.all().order_by('id'):
            userinfo = user.getUserInfo()
            if userinfo:
                has_password = _has_password(user)
                screenName = userinfo.screenName
                new_username = slugify(screenName)
                new_is_valid = user_services.is_valid_username(new_username)
                if has_password:
                    _user_with_password(user)
                elif screenName == new_username:
                    _user_with_same_screenName_already(user)
                elif not new_is_valid:
                    _user_with_invalid_screenName(user)
                else:
                    _user_default(user)
