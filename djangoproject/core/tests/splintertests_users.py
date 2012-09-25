from time import sleep
import traceback
from helpers import testdata as td
from splintertests_issues import FrespoSplinterTestCase
from unittest import skipIf
from django.conf import settings

waitifbreak = 10

__author__ = 'tony'

@skipIf(settings.SKIP_GOOGLE_TESTS)
class AccountCreationTests(FrespoSplinterTestCase):
    def needs_users(self):
        return False

    def test_splinter_createaccount(self):
        try:
            self.app.create_account_google(td.userDict1)
        except:
            traceback.print_exc()
            sleep(waitifbreak)
            raise