from core.models import *
from django.utils import unittest
from core.services import watch_services
from helpers import test_data, email_asserts
from django.test.client import Client

__author__ = 'tony'

class TestMailNotifications(unittest.TestCase):
    def setUp(self):
        # Every test needs a client.
        self.user = test_data.createDummyUserRandom(login='johndoe', password='abc123')
        self.client = Client()
        self.client.login(username=self.user.username, password='abc123')

    def test_should_send_mail_for_new_comments(self):
        offer = test_data.create_dummy_offer()
        issue = offer.issue
        response = self.client.get('/core/watch/issue/%s'%issue.id)
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/core/watch/offer/%s'%offer.id)
        self.assertEqual(response.status_code, 200)

        user2 = test_data.createDummyUserRandom(login='marydoe', password='xyz456')
        client2 = Client()
        client2.login(username=user2.username, password='xyz456')

        email_asserts.clear_sent()
        response = client2.post('/core/issue/comment/add/submit', {'issue_id': str(issue.id), 'content': 'Im adding a comment'})
        self.assertEqual(response.status_code, 302)

        email_asserts.send_emails()
        email_asserts.assert_sent_count(self, 1)
        email_asserts.assert_sent(self, to=self.user.email, subject="%s added a comment on issue [%s]"%(user2.getUserInfo().screenName, issue.title))

        email_asserts.clear_sent()
        response = client2.post('/core/offer/comment/add/submit', {'offer_id': str(offer.id), 'content': 'Im adding another comment'})
        self.assertEqual(response.status_code, 302)

        email_asserts.send_emails()
        email_asserts.assert_sent_count(self, 1)
        email_asserts.assert_sent(self, to=self.user.email, subject="%s added a comment on offer [US$ %s / %s]"%(user2.getUserInfo().screenName, '10.00', issue.title))

    def test_should_send_mail_for_adding_or_changing_or_revoking_offer(self):
        offer = test_data.create_dummy_offer()
        issue = offer.issue
        response = self.client.get('/core/watch/issue/%s'%issue.id)
        self.assertEqual(response.status_code, 200)

        user2 = test_data.createDummyUserRandom(login='marydoe', password='xyz456')
        user2ScreenName = user2.getUserInfo().screenName
        client2 = Client()
        client2.login(username=user2.username, password='xyz456')

        email_asserts.clear_sent()
        response = client2.post('/core/issue/sponsor/submit',
            {'issue_id': str(issue.id),
             'price':'20.00',
             'currency' : 'USD',
             'acceptanceCriteria':'some criteria',})
        self.assertEqual(response.status_code, 302)
        offer_id = response.get('location').split('/')[-2]

        email_asserts.send_emails()
        email_asserts.assert_sent_count(self, 2) #one to the watcher, other to the site admin
        email_asserts.assert_sent(self, to=self.user.email, subject="%s made a US$ 20.00 offer for issue [%s]"%(user2ScreenName, issue.title))

        email_asserts.clear_sent()
        response = client2.post('/core/offer/edit/submit',
            {'offer_id': offer_id,
             'price':'30.00',
             'acceptanceCriteria':'some criteria',})
        self.assertEqual(response.status_code, 302)
        email_asserts.send_emails()
        email_asserts.assert_sent_count(self, 1)
        email_asserts.assert_sent(self, to=self.user.email, subject="%s raised the US$ 20.00 offer on issue [%s]"%(user2ScreenName, issue.title))

        email_asserts.clear_sent()
        response = client2.post('/core/offer/revoke/submit',
            {'offer_id': offer_id,
             'comment' : ''})
        self.assertEqual(response.status_code, 302)
        email_asserts.send_emails()
        email_asserts.assert_sent_count(self, 1)
        email_asserts.assert_sent(self, to=self.user.email, subject="%s revoked his US$ 30.00 offer for issue [%s]"%(user2ScreenName, issue.title))

    def test_should_send_mail_for_starting_or_aborting_or_finishing_work(self):
        offer = test_data.create_dummy_offer()
        issue = offer.issue
        response = self.client.get('/core/watch/issue/%s'%issue.id)
        self.assertEqual(response.status_code, 200)

        user2 = test_data.createDummyUserRandom(login='marydoe', password='xyz456')
        user2ScreenName = user2.getUserInfo().screenName
        client2 = Client()
        client2.login(username=user2.username, password='xyz456')

        #STARTS WORKING
        email_asserts.clear_sent()
        response = client2.post('/core/solution/add/submit',
            {'issue_id': str(issue.id),
             'comment':''})
        self.assertEqual(response.status_code, 302)
        issue_id = response.get('location').split('/')[-2]
        response = client2.get('/core/issue/%s/blah'%issue_id)
        solution_id = str(response.context['mysolution'].id)

        email_asserts.send_emails()
        email_asserts.assert_sent_count(self, 1)
        email_asserts.assert_sent(self, to=self.user.email, subject="%s has just begun working on issue [%s]"%(user2ScreenName, issue.title))

        #ABORTS WORK
        email_asserts.clear_sent()
        response = client2.post('/core/solution/abort/submit',
            {'solution_id': solution_id,
             'comment':''})
        self.assertEqual(response.status_code, 302)

        email_asserts.send_emails()
        email_asserts.assert_sent_count(self, 1)
        email_asserts.assert_sent(self, to=self.user.email, subject="%s has stopped working on issue [%s]"%(user2ScreenName, issue.title))

        #STARTS WORKING again
        email_asserts.clear_sent()
        response = client2.post('/core/solution/add/submit',
            {'issue_id': str(issue.id),
             'comment':''})
        self.assertEqual(response.status_code, 302)
        issue_id = response.get('location').split('/')[-2]
        response = client2.get('/core/issue/%s/blah'%issue_id)
        solution_id2 = str(response.context['mysolution'].id)
        self.assertEqual(solution_id, solution_id2)

        email_asserts.send_emails()
        email_asserts.assert_sent_count(self, 1)
        email_asserts.assert_sent(self, to=self.user.email, subject="%s has just begun working on issue [%s]"%(user2ScreenName, issue.title))

        #FINISHES WORK
        email_asserts.clear_sent()
        response = client2.post('/core/solution/resolve/submit',
            {'solution_id': solution_id,
             'comment':''})
        self.assertEqual(response.status_code, 302)

        email_asserts.send_emails()
        email_asserts.assert_sent_count(self, 1)
        email_asserts.assert_sent(self, to=self.user.email, subject="%s resolved issue [%s]"%(user2ScreenName, issue.title))
