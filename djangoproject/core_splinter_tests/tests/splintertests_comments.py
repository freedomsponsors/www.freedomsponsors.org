from time import sleep
from decimal import Decimal
from core.management.commands.loadProjects import add_initial_projects
from splintertests_issues import FrespoSplinterTestCase
from helpers import testdata as td
import traceback

__author__ = 'tony'

waitifbreak = 1

class SoloUserCommentTests(FrespoSplinterTestCase):
#    def onAppCreate(self):
#        self.app.createGoogleSession(td.userDict1)

    def test_splinter_solo_comments(self):
        add_initial_projects()
        offer = td.buildOfferForHHH1052(self.users[0].adminUser)
        td.loadOffer(offer)
        self.app.login_plain(td.userDict1)
        try:
            self.app.followSponsoringIssueLinkOnHomeByTitle('Allow CalendarType.set to accept Date objects')
            def gogogo():
                self.app.commentOnCurrentIssueOrOffer('Hello comment')
                assert(self.app.is_text_present('Hello comment'))
                comment = '''
I am another comment

    def pyfunc():
        print 'blag'

another text

    <script>alert('hi')</script>
                '''
                self.app.commentOnCurrentIssueOrOffer(comment, 'I am another comment')
                assert(self.app.is_text_present('Hello comment'))
                assert(self.app.is_text_present('I am another comment'))
                assert(self.app.is_text_present('def pyfunc():'))
                assert(self.app.is_text_present("<script>alert('hi')</script>"))
                self.app.editCommentOnCurrentIssueOrOffer(0, 'Howdy comment')
                assert(not self.app.is_text_present('Hello comment'))
                assert(self.app.is_text_present('Howdy comment'))
                self.app.editCommentOnCurrentIssueOrOffer(1, 'bilubilu')
                assert(not self.app.is_text_present('I am another comment'))
                assert(not self.app.is_text_present("<script>alert('hi')</script>"))
                assert(self.app.is_text_present('bilubilu'))

            gogogo()
            self.app.followOfferLinkByValue(Decimal('10.00'))
            gogogo()
        except:
            traceback.print_exc()
            sleep(waitifbreak)
            raise
