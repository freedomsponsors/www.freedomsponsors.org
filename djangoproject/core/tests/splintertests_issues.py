from decimal import Decimal
from time import sleep
import traceback
from django.test import LiveServerTestCase
from core.management.commands.loadFeedbackData import frespoProject, frespoUser
from core.management.commands.loadProjects import add_initial_projects
from helpers import testdata as td
from helpers.appdriver import AppDriver

waitifbreak = 10

__author__ = 'tony'

class FrespoSplinterTestCase(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = None
        super(FrespoSplinterTestCase, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.app.quit()
        super(FrespoSplinterTestCase, cls).tearDownClass()

    def setUp(self):
        if(not self.__class__.app):
            self.app = AppDriver.build()
            self.__class__.app = self.app
            self.onAppCreate()
        if self.needs_users():
            self.users = td.loadUsersPlain()
        self.app.reset(self.live_server_url)

    def tearDown(self):
        self.app.logout()

    def onAppCreate(self):
        pass

    def needs_users(self):
        return True

class SecondUserIssueTests(FrespoSplinterTestCase):
#    def onAppCreate(self):
#        self.app.createGoogleSession(td.userDict2)

    def test_splinter_sponsor_issue_HHH_1052(self):
        add_initial_projects()
        offer = td.buildOfferForHHH1052(self.users[0].adminUser)
        td.loadOffer(offer)
        try:
            self.app.login_plain(td.userDict2)
            self.app.followIssueLinkOnHomeByTitle('Allow CalendarType.set to accept Date objects')
            otherOffer = {
                'price':Decimal('15.00'),
                'acceptanceCriteria':'Soh comitar',
                'require_release' : False,
                'no_forking' : True,
            }
            self.app.sponsorCurrentIssue(otherOffer)
            assert(self.app.is_text_present('[ Offer ] US$ 15.00 for issue - Allow CalendarType.set to accept Date objects'))
            self.app.followIssueLinkOnHomeByTitle('Allow CalendarType.set to accept Date objects')
            self.app.followOfferLinkByValue(otherOffer['price'])
        except:
            traceback.print_exc()
            sleep(waitifbreak)
            raise


class SoloUserIssueTests(FrespoSplinterTestCase):
#    def onAppCreate(self):
#        self.app.createGoogleSession(td.userDict1)

    def test_splinter_login(self):
        self.app.login_plain(td.userDict1)

    def test_splinter_add_issue_HHH_1052(self):
        add_initial_projects()
        self.app.login_plain(td.userDict1)
        try:
            offerDict = td.buildDefaultOfferDict14('https://hibernate.onjira.com/browse/HHH-1052')
            self.app.addOffer(offerDict)
            assert(self.app.is_text_present('[ Offer ] US$ 10.00 for issue - Allow CalendarType.set to accept Date objects'))
            self.app.followIssueLinkOnHomeByTitle('Allow CalendarType.set to accept Date objects')
            self.app.followOfferLinkByValue(offerDict['step4']['price'])
        except:
            traceback.print_exc()
            sleep(waitifbreak)
            raise

    def test_splinter_sponsor_jira_HHH0152(self):
        add_initial_projects()
        self.app.login_plain(td.userDict1)
        try:
            offerDict = td.buildDefaultOfferDict14('https://hibernate.onjira.com/browse/HHH-1052')
            del offerDict['step1']
            self.app.sponsor_issue('https://hibernate.onjira.com/browse/HHH-1052', offerDict)
            assert(self.app.is_text_present('[ Offer ] US$ 10.00 for issue - Allow CalendarType.set to accept Date objects'))
            self.app.followIssueLinkOnHomeByTitle('Allow CalendarType.set to accept Date objects')
            self.app.followOfferLinkByValue(offerDict['step4']['price'])
        except:
            traceback.print_exc()
            sleep(waitifbreak)
            raise


    def test_splinter_add_issue_HHH_1052_with_empty_db(self):
        frespoProject(frespoUser())
        self.app.login_plain(td.userDict1)
        try:
            self.app.go_to_projects()
            assert(not self.app.is_text_present('Hibernate'))
            offerDict = td.buildDefaultOfferDict134(trackerURL='https://hibernate.onjira.com/browse/HHH-1052',
                newProjectHomeURL='http://www.hibernate.org/')
            self.app.addOffer(offerDict)
            assert(self.app.is_text_present('[ Offer ] US$ 10.00 for issue - Allow CalendarType.set to accept Date objects'))
            self.app.followIssueLinkOnHomeByTitle('Allow CalendarType.set to accept Date objects')
            self.app.followOfferLinkByValue(offerDict['step4']['price'])
            self.app.go_to_projects()
            assert(self.app.is_text_present('Hibernate ORM'))
            assert(self.app.is_text_present('http://www.hibernate.org/'))
        except:
            traceback.print_exc()
            sleep(waitifbreak)
            raise

    def test_splinter_add_issue_inexistent(self):
        frespoProject(frespoUser())
        self.app.login_plain(td.userDict1)
        try:
            offerDict = td.buildDefaultOfferDict1234(
                trackerURL='https://hibernate.onjira.com/browse/OH404-1052',
                key='OH404-1052',
                title='This issue does not exist anywhere',
                newProjectName='Hibernatis',
                newProjectHomeURL='http://www.hibernate.org/',
                newProjectTrackerURL='https://hibernate.onjira.com/browse/OH404')
            self.app.addOffer(offerDict)
            assert(self.app.is_text_present('[ Offer ] US$ 10.00 for issue - This issue does not exist anywhere'))
            self.app.followIssueLinkOnHomeByTitle('This issue does not exist anywhere')
            self.app.followOfferLinkByValue(offerDict['step4']['price'])
            self.app.go_to_projects()
            assert(self.app.is_text_present('Hibernatis'))
            assert(self.app.is_text_present('http://www.hibernate.org/'))
            assert(self.app.is_text_present('https://hibernate.onjira.com/browse/OH404'))
        except:
            traceback.print_exc()
            sleep(waitifbreak)
            raise

    def test_splinter_add_issue_unreachable(self):
        frespoProject(frespoUser())
        self.app.login_plain(td.userDict1)
        try:
            offerDict = td.buildDefaultOfferDict1234(
                trackerURL='https://hibernatis.onjira.com/browse/OH404-1052',
                key='OH404-1052',
                title='This issue is on an unreachable tracker',
                newProjectName='Hibernatis',
                newProjectHomeURL='http://www.hibernate.org/',
                newProjectTrackerURL='https://hibernate.onjira.com/browse/OH404')
            self.app.addOffer(offerDict)
            assert(self.app.is_text_present('[ Offer ] US$ 10.00 for issue - This issue is on an unreachable tracker'))
            self.app.followIssueLinkOnHomeByTitle('This issue is on an unreachable tracker')
            self.app.followOfferLinkByValue(offerDict['step4']['price'])
            self.app.go_to_projects()
            assert(self.app.is_text_present('Hibernatis'))
            assert(self.app.is_text_present('http://www.hibernate.org/'))
            assert(self.app.is_text_present('https://hibernate.onjira.com/browse/OH404'))
        except:
            traceback.print_exc()
            sleep(waitifbreak)
            raise

    def test_splinter_add_issue_avulsa(self):
        self.app.login_plain(td.userDict1)
        try:
            offerDict = td.buildOfferDictAvulsa()
            self.app.addOffer(offerDict)
            assert(self.app.is_text_present('[ Offer ] US$ 10.00 for issue - Build me a teleporting machine'))
            self.app.followIssueLinkOnHomeByTitle('Build me a teleporting machine')
            self.app.followOfferLinkByValue(offerDict['step4']['price'])
        except:
            traceback.print_exc()
            sleep(waitifbreak)
            raise

    def test_splinter_edit_issue_HHH_1052(self):
        add_initial_projects()
        offer = td.buildOfferForHHH1052(self.users[0].adminUser)
        td.loadOffer(offer)
        self.app.login_plain(td.userDict1)
        try:
            self.app.followIssueLinkOnHomeByTitle('Allow CalendarType.set to accept Date objects')

            self.app.editCurrentOffer(price=Decimal('11.00'), expires=True, expiration_days=2)
            assert(self.app.is_text_present('[ Offer ] US$ 11.00 for issue - Allow CalendarType.set to accept Date objects'))
            assert(self.app.is_text_present('EXPIRES ON '))

            self.app.editCurrentOffer(expires=False)
            assert(self.app.is_text_present('[ Offer ] US$ 11.00 for issue - Allow CalendarType.set to accept Date objects'))
            assert(not self.app.is_text_present('EXPIRES ON '))

            self.app.editCurrentOffer(no_forking=True, require_release=False)
            assert(self.app.is_text_present('[ Offer ] US$ 11.00 for issue - Allow CalendarType.set to accept Date objects'))
            assert(self.app.is_text_present('NO FORKING'))
            assert(not self.app.is_text_present('RELEASE REQUIRED'))
            assert(not self.app.is_text_present('EXPIRES ON '))

            self.app.editCurrentOffer(no_forking=False, require_release=True)
            assert(self.app.is_text_present('[ Offer ] US$ 11.00 for issue - Allow CalendarType.set to accept Date objects'))
            assert(not self.app.is_text_present('NO FORKING'))
            assert(self.app.is_text_present('RELEASE REQUIRED'))
            assert(not self.app.is_text_present('EXPIRES ON '))

            self.app.editCurrentOffer(price=Decimal('100'), expires=True, expiration_days=200)
            assert(self.app.is_text_present('[ Offer ] US$ 100.00 for issue - Allow CalendarType.set to accept Date objects'))
            assert(not self.app.is_text_present('NO FORKING'))
            assert(self.app.is_text_present('RELEASE REQUIRED'))
            assert(self.app.is_text_present('EXPIRES ON '))

        except:
            traceback.print_exc()
            sleep(waitifbreak)
            raise