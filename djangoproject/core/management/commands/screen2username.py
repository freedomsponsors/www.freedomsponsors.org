from django.contrib.auth.models import User
from django.core.management.base import NoArgsCommand
from optparse import make_option
from django.template.base import Template
from django.template.context import Context
from django.template.defaultfilters import slugify
from core.services import user_services, mail_services

BODY_USER_WITH_PASSWORD = """
TODO
"""

BODY_USER_WITH_SAME_SCREENNAME = """
TODO
"""

BODY_USER_WITH_INVALID_SCREENNAME = """
TODO
"""

BODY_USER_DEFAULT = """
TODO
"""


def _has_password(user):
    return user.password and len(user.password) > 1


def _template_render(source, user):
    t = Template(source)
    body = t.render(Context({'user': user}))
    return body


def _user_with_password(user):
    subject = 'Important information about your account on FreedomSponsors'
    body = _template_render(BODY_USER_WITH_PASSWORD, user)
    mail_services.plain_send_mail(user.email, subject, body)


def _user_with_same_screenName_already(user):
    subject = 'Important information about your account on FreedomSponsors'
    body = _template_render(BODY_USER_WITH_SAME_SCREENNAME, user)
    mail_services.plain_send_mail(user.email, subject, body)


def _user_with_invalid_screenName(user):
    # TODO: set username
    subject = 'Important information about your account on FreedomSponsors'
    body = _template_render(BODY_USER_WITH_INVALID_SCREENNAME, user)
    mail_services.plain_send_mail(user.email, subject, body)


def _user_default(user):
    # TODO: set username
    subject = 'Important information about your account on FreedomSponsors'
    body = _template_render(BODY_USER_DEFAULT, user)
    mail_services.plain_send_mail(user.email, subject, body)


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
