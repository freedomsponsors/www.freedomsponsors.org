from core.models import Project, User, Issue
from django.test import TestCase

USER_NAME = 'test_user'
USER_MAIL = 'mail@mail.com.zz'
USER_PASS = 'secret'

PROJECT_NAME = 'project_name'
PROJECT_URL = 'http://localhost/fs'
PROJECT_BUGTRACKER = 'http://localhost/bugtracker'

ISSUE_KEY = 'ISSUEID'
ISSUE_TITLE = 'first_issue'
ISSUE_DESCRIPTION = 'a description'

class TestUser(TestCase):
    
    def setUp(self):
        try:
            self.user = User.objects.get_by_natural_key(USER_NAME)
        except:
            self.user = User.objects.create_user(USER_NAME, USER_MAIL, USER_PASS)
        
    def test_user_name(self):
        self.assertEquals(self.user.username, USER_NAME)
    
    def test_user_mail(self):
        self.assertEquals(self.user.email, USER_MAIL)

    def test_user_pass(self):
        #self.assertEquals(self.user.password, TestUser.USER_PASS)
        #TODO: test password generation
        pass

class TestProject(TestCase):
    
    def setUp(self):
        try:
            self.user = User.objects.get_by_natural_key(USER_NAME)
        except:
            self.user = User.objects.create_user(USER_NAME, USER_MAIL, USER_PASS)
        self.project = Project.newProject(PROJECT_NAME, self.user, PROJECT_URL, PROJECT_BUGTRACKER)
    
    def test_project_name(self):
        self.assertEqual(self.project.name, PROJECT_NAME)
        
    def test_project_user(self):
        self.assertEqual(self.project.createdByUser.id, self.user.id)
    
    def test_project_url(self):
        self.assertEquals(self.project.homeURL, PROJECT_URL)
        
    def test_project_bugtracking_url(self):
        self.assertEquals(self.project.trackerURL, PROJECT_BUGTRACKER)
     
class TestIssue(TestCase):
    
    def setUp(self):
        try:
            self.user = User.objects.get_by_natural_key(USER_NAME)
        except:
            self.user = User.objects.create_user(USER_NAME, USER_MAIL, USER_PASS)
        self.project = Project.newProject(PROJECT_NAME, self.user, PROJECT_URL, PROJECT_BUGTRACKER)
        self.issue = Issue.newIssue(self.project, ISSUE_KEY, ISSUE_TITLE, ISSUE_DESCRIPTION, self.project.createdByUser, self.project.trackerURL)
        
    def test_issue_project(self):
        self.assertEquals(self.issue.project, self.project)
    
    def test_issue_key(self):
        self.assertEquals(self.issue.key, ISSUE_KEY)
        
    def test_issue_title(self):
        self.assertEqual(self.issue.title, ISSUE_TITLE)
        
    def test_issue_user(self):
        self.assertEqual(self.issue.createdByUser, self.project.createdByUser)
    
    def test_issue_tracker_url(self):
        self.assertEquals(self.issue.trackerURL, self.project.trackerURL)