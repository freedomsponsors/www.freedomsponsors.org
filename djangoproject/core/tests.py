from django.test import TestCase
from django.conf import settings
from core.models import *
from time import sleep
from decimal import Decimal
import traceback
from django.test import LiveServerTestCase
from core.testinghelpers.appdriver import AppDriver
from core.testinghelpers import testdata as td
from core.management.commands.loadProjects import add_initial_projects
from core.management.commands.loadFeedbackData import frespoUser, frespoProject
from trackerutils import fetchIssueInfo

waitifbreak=10

class TrackerUtilsTest(TestCase):
    def test_hibernate_jira(self):
        issueInfo = fetchIssueInfo("https://hibernate.onjira.com/browse/HHH-1050")
        assert(not issueInfo.error)
        assert(issueInfo.tracker == 'JIRA')
        assert(issueInfo.key == 'HHH-1050')
        assert(issueInfo.project_trackerURL == 'https://hibernate.onjira.com/browse/HHH')
        assert(issueInfo.project_name == 'Hibernate ORM')
        assert(issueInfo.issue_title == 'HQL Unions')

    def test_jenkins_jira(self):
        issueInfo = fetchIssueInfo("https://issues.jenkins-ci.org/browse/JENKINS-9216")
        assert(not issueInfo.error)
        assert(issueInfo.tracker == 'JIRA')
        assert(issueInfo.key == 'JENKINS-9216')
        assert(issueInfo.project_trackerURL == 'https://issues.jenkins-ci.org/browse/JENKINS')
        assert(issueInfo.project_name == 'Jenkins')
        assert(issueInfo.issue_title == 'Make OpenID work with Google Apps accounts')

    def test_maven_jira(self):
        issueInfo = fetchIssueInfo("http://jira.codehaus.org/browse/MNG-5121")
        assert(not issueInfo.error)
        assert(issueInfo.tracker == 'JIRA')
        assert(issueInfo.key == 'MNG-5121')
        assert(issueInfo.project_trackerURL == 'http://jira.codehaus.org/browse/MNG')
        assert(issueInfo.project_name == 'Maven 2 & 3')
        assert(issueInfo.issue_title == 'maven seems to lose transitive dependencies from the list of compilation dependencies')

    def test_easymock_jira(self):
        issueInfo = fetchIssueInfo("http://jira.codehaus.org/browse/EASYMOCK-111")
        assert(not issueInfo.error)
        assert(issueInfo.tracker == 'JIRA')
        assert(issueInfo.key == 'EASYMOCK-111')
        assert(issueInfo.project_trackerURL == 'http://jira.codehaus.org/browse/EASYMOCK')
        assert(issueInfo.project_name == 'EasyMock')
        assert(issueInfo.issue_title == 'Calling behaviour more than expected number of times does not assert failure when the call is from multple threads')

    def test_axis_jira(self):
        issueInfo = fetchIssueInfo("https://issues.apache.org/jira/browse/AXIS-66")
        assert(not issueInfo.error)
        assert(issueInfo.tracker == 'JIRA')
        assert(issueInfo.key == 'AXIS-66')
        assert(issueInfo.project_trackerURL == 'https://issues.apache.org/jira/browse/AXIS')
        assert(issueInfo.project_name == 'Axis')
        assert(issueInfo.issue_title == '[xsd:list] WSDL2Java doesn\'t handle schema <list> enumerations')

    def test_p2d_jira(self):
        issueInfo = fetchIssueInfo("https://jira.p2d.com.br/browse/PORTAL-300")
        assert(issueInfo.error)
        assert(issueInfo.tracker == 'JIRA')
        assert(issueInfo.key == 'PORTAL-300')
        assert(issueInfo.project_trackerURL == 'https://jira.p2d.com.br/browse/PORTAL')
        # assert(issueInfo.project_name == 'blau')
        # assert(issueInfo.issue_title == 'blau')

    def test_gittip_github(self):
        issueInfo = fetchIssueInfo("https://github.com/whit537/www.gittip.com/issues/14")
        assert(not issueInfo.error)
        assert(issueInfo.tracker == 'GITHUB')
        assert(issueInfo.key == '14')
        assert(issueInfo.project_trackerURL == 'https://github.com/whit537/www.gittip.com/issues')
        assert(issueInfo.project_name == 'www.gittip.com')
        assert(issueInfo.issue_title == 'pay with bitcoin, litecoin')

    def test_ant_bugzilla(self):
        issueInfo = fetchIssueInfo("https://issues.apache.org/bugzilla/show_bug.cgi?id=32089")
        assert(not issueInfo.error)
        assert(issueInfo.tracker == 'BUGZILLA')
        assert(issueInfo.key == '32089')
        assert(issueInfo.project_trackerURL == 'https://issues.apache.org/bugzilla/buglist.cgi?product=Ant')
        assert(issueInfo.project_name == 'Ant')
        assert(issueInfo.issue_title == 'stcheckout sometimes creates folders instead of files then throws exception')

    def test_nowhere(self):
        issueInfo = fetchIssueInfo("https://theres.nothing.here/jira/browse/NOTHING-123")
        assert(issueInfo.error)

class AccountCreationTests(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = None
        super(AccountCreationTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.app.quit()

    def setUp(self):
        if(not AccountCreationTests.app):
            self.app = AppDriver.build()
            AccountCreationTests.app = self.app
        self.app.reset(self.live_server_url)

    def tearDown(self):
        self.app.logout()

    def test_splinter_createaccount(self):
        try:
            self.app.create_account_google(td.userDict1)
        except:
            traceback.print_exc()
            sleep(waitifbreak)
            raise

class SoloUserTests(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = None
        super(SoloUserTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.app.quit()

    def setUp(self):
        if(not SoloUserTests.app):
            self.app = AppDriver.build()
            SoloUserTests.app = self.app
            self.app.createGoogleSession(td.userDict1)
        self.users = td.loadUsers()
        self.app.reset(self.live_server_url)

    def tearDown(self):
        self.app.logout()

    def test_splinter_login(self):
        self.app.login_google()
        
    def test_splinter_add_issue_HHH_1052(self):
        add_initial_projects()
        # td.loadUsers()
        self.app.login_google()
        try:
            offerDict = td.buildDefaultOfferDict14('https://hibernate.onjira.com/browse/HHH-1052')
            self.app.addOffer(offerDict)
            assert(self.app.is_text_present('[ Offer ] U$ 10.00 for issue - Allow CalendarType.set to accept Date objects'))
            self.app.followIssueLinkOnHomeByTitle('Allow CalendarType.set to accept Date objects')
            self.app.followOfferLinkByValue(offerDict['step4']['price'])
        except:
            traceback.print_exc()
            sleep(waitifbreak)
            raise

    def test_splinter_sponsor_jira_HHH0152(self):
        add_initial_projects()
        # td.loadUsers()
        self.app.login_google()
        try:
            offerDict = td.buildDefaultOfferDict14('https://hibernate.onjira.com/browse/HHH-1052')
            del offerDict['step1']
            self.app.sponsor_issue('https://hibernate.onjira.com/browse/HHH-1052', offerDict)
            assert(self.app.is_text_present('[ Offer ] U$ 10.00 for issue - Allow CalendarType.set to accept Date objects'))
            self.app.followIssueLinkOnHomeByTitle('Allow CalendarType.set to accept Date objects')
            self.app.followOfferLinkByValue(offerDict['step4']['price'])
        except:
            traceback.print_exc()
            sleep(waitifbreak)
            raise

    def test_splinter_add_issue_HHH_1052_with_empty_db(self):
        # td.loadUsers()
        frespoProject(frespoUser())
        self.app.login_google()
        try:
            self.app.go_to_projects()
            assert(not self.app.is_text_present('Hibernate'))
            offerDict = td.buildDefaultOfferDict134(trackerURL='https://hibernate.onjira.com/browse/HHH-1052', 
                newProjectHomeURL='http://www.hibernate.org/')
            self.app.addOffer(offerDict)
            assert(self.app.is_text_present('[ Offer ] U$ 10.00 for issue - Allow CalendarType.set to accept Date objects'))
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
        # td.loadUsers()
        frespoProject(frespoUser())
        self.app.login_google()
        try:
            offerDict = td.buildDefaultOfferDict1234(
                trackerURL='https://hibernate.onjira.com/browse/OH404-1052',
                key='OH404-1052',
                title='This issue does not exist anywhere',
                newProjectName='Hibernatis',
                newProjectHomeURL='http://www.hibernate.org/',
                newProjectTrackerURL='https://hibernate.onjira.com/browse/OH404')
            self.app.addOffer(offerDict)
            assert(self.app.is_text_present('[ Offer ] U$ 10.00 for issue - This issue does not exist anywhere'))
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
        # td.loadUsers()
        frespoProject(frespoUser())
        self.app.login_google()
        try:
            offerDict = td.buildDefaultOfferDict1234(
                trackerURL='https://hibernatis.onjira.com/browse/OH404-1052',
                key='OH404-1052',
                title='This issue is on an unreachable tracker',
                newProjectName='Hibernatis',
                newProjectHomeURL='http://www.hibernate.org/',
                newProjectTrackerURL='https://hibernate.onjira.com/browse/OH404')
            self.app.addOffer(offerDict)
            assert(self.app.is_text_present('[ Offer ] U$ 10.00 for issue - This issue is on an unreachable tracker'))
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
        # td.loadUsers()
        self.app.login_google()
        try:
            offerDict = td.buildOfferDictAvulsa()
            self.app.addOffer(offerDict)
            assert(self.app.is_text_present('[ Offer ] U$ 10.00 for issue - Build me a teleporting machine'))
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
        self.app.login_google()
        try:
            self.app.followIssueLinkOnHomeByTitle('Allow CalendarType.set to accept Date objects')

            self.app.editCurrentOffer(price=Decimal('11.00'), expires=True, expiration_days=2)
            assert(self.app.is_text_present('[ Offer ] U$ 11.00 for issue - Allow CalendarType.set to accept Date objects'))
            assert(self.app.is_text_present('EXPIRES ON '))

            self.app.editCurrentOffer(expires=False)
            assert(self.app.is_text_present('[ Offer ] U$ 11.00 for issue - Allow CalendarType.set to accept Date objects'))
            assert(not self.app.is_text_present('EXPIRES ON '))

            self.app.editCurrentOffer(no_forking=True, require_release=False)
            assert(self.app.is_text_present('[ Offer ] U$ 11.00 for issue - Allow CalendarType.set to accept Date objects'))
            assert(self.app.is_text_present('NO FORKING'))
            assert(not self.app.is_text_present('RELEASE REQUIRED'))
            assert(not self.app.is_text_present('EXPIRES ON '))
            
            self.app.editCurrentOffer(no_forking=False, require_release=True)
            assert(self.app.is_text_present('[ Offer ] U$ 11.00 for issue - Allow CalendarType.set to accept Date objects'))
            assert(not self.app.is_text_present('NO FORKING'))
            assert(self.app.is_text_present('RELEASE REQUIRED'))
            assert(not self.app.is_text_present('EXPIRES ON '))
            
            self.app.editCurrentOffer(price=Decimal('100'), expires=True, expiration_days=200)
            assert(self.app.is_text_present('[ Offer ] U$ 100.00 for issue - Allow CalendarType.set to accept Date objects'))
            assert(not self.app.is_text_present('NO FORKING'))
            assert(self.app.is_text_present('RELEASE REQUIRED'))
            assert(self.app.is_text_present('EXPIRES ON '))
            
        except:
            traceback.print_exc()
            sleep(waitifbreak)
            raise
            

class SecondUserTests(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = None
        super(SecondUserTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.app.quit()

    def setUp(self):
        if(not SecondUserTests.app):
            self.app = AppDriver.build()
            SecondUserTests.app = self.app
            self.app.createGoogleSession(td.userDict2)
        self.users = td.loadUsers()
        self.app.reset(self.live_server_url)

    def test_splinter_sponsor_issue_HHH_1052(self):
        add_initial_projects()
        # users = td.loadUsers()
        offer = td.buildOfferForHHH1052(self.users[0].adminUser)
        td.loadOffer(offer)
        try:
            self.app.login_google()
            self.app.followIssueLinkOnHomeByTitle('Allow CalendarType.set to accept Date objects')
            otherOffer = {
                'price':Decimal('15.00'), 
                'acceptanceCriteria':'Soh comitar',
                'require_release' : False,
                'no_forking' : True,
            }
            self.app.sponsorCurrentIssue(otherOffer)
            assert(self.app.is_text_present('[ Offer ] U$ 15.00 for issue - Allow CalendarType.set to accept Date objects'))
            self.app.followIssueLinkOnHomeByTitle('Allow CalendarType.set to accept Date objects')
            self.app.followOfferLinkByValue(otherOffer['price'])
        except:
            traceback.print_exc()
            sleep(waitifbreak)
            raise
