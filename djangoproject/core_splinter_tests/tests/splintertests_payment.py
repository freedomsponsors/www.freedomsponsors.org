from time import sleep
from decimal import Decimal
from core.management.commands.loadProjects import add_initial_projects
from splintertests_issues import FrespoSplinterTestCase
from django.test import LiveServerTestCase
from helpers import testdata as td
from django.utils.unittest import skipIf
from frespo import env_settings
import traceback

__author__ = 'tony'

waitifbreak = 1

@skipIf(env_settings.ENVIRONMENT != 'DEV', 'not supported in this environment')
class PaymentTests(FrespoSplinterTestCase):
#    def onAppCreate(self):
#        self.app.createGoogleSession(td.userDict1)

    def test_pay_with_paypal(self):
        add_initial_projects()
        offer = td.buildOfferForHHH1052(self.users[0].adminUser)
        td.loadOffer(offer)
        solution = td.buildSolutionDoneFor(offer.issue, self.users[1].adminUser, True)
        td.loadSolution(solution)
        try:
            self.app.login_plain(td.userDict1)
            self.app.followIssueLinkOnHomeByTitle('Allow CalendarType.set to accept Date objects')
            self.app.pay_with_paypal(td.paypal_credentials_1)
            self.app.followIssueLinkOnHomeByTitle('Allow CalendarType.set to accept Date objects')
            sleep(10)
#            assert(self.app.is_text_present('10.00'))
#            assert(self.app.is_text_present('PAID'))
        except:
            traceback.print_exc()
            sleep(waitifbreak)
            raise
