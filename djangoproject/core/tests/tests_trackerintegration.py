from django.test import TestCase
from core.utils.trackers_adapter import fetchIssueInfo
from django.utils.unittest import skipIf
from django.conf import settings

__author__ = 'tony'

@skipIf(settings.SKIPTESTS_TRACKERINTEGRATION == True, 'Skipped as requested by SKIPTESTS_TRACKERINTEGRATION in settings.py')
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
        assert(issueInfo.project_name == 'Maven')
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
        issueInfo = fetchIssueInfo("https://github.com/gittip/www.gittip.com/issues/14")
        assert(not issueInfo.error)
        assert(issueInfo.tracker == 'GITHUB')
        assert(issueInfo.key == '14')
        assert(issueInfo.project_trackerURL == 'https://github.com/gittip/www.gittip.com/issues')
        assert(issueInfo.project_name == 'www.gittip.com')
        assert(issueInfo.issue_title == 'pay in with bitcoin')

    def test_coveragepy_bitbucket(self):
        issueInfo = fetchIssueInfo("https://bitbucket.org/ned/coveragepy/issue/193/unicodedecodeerror-on-htmlpy")
        assert(not issueInfo.error)
        assert(issueInfo.tracker == 'BITBUCKET')
        assert(issueInfo.key == '193')
        assert(issueInfo.project_trackerURL == 'https://bitbucket.org/ned/coveragepy/issues')
        assert(issueInfo.project_name == 'coveragepy')
        assert(issueInfo.issue_title == 'UnicodeDecodeError on html.py')

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

    def test_chromium_googlecode(self):
        issueInfo = fetchIssueInfo("http://code.google.com/p/chromium/issues/detail?id=140028")
        assert not issueInfo.error
        assert issueInfo.tracker == 'GOOGLECODE'
        assert issueInfo.key == '140028'
        assert issueInfo.project_trackerURL == 'http://code.google.com/p/chromium/issues/list'
        assert issueInfo.project_name == 'chromium'
        assert issueInfo.issue_title == 'Slow memory leak seen when Google Analytics loaded in Chrome with Real Time view'
