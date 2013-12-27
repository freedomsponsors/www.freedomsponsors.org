from django.test import TestCase
from core.services import watch_services
from helpers import test_data
from django.test.client import Client
from django.core.urlresolvers import reverse

__author__ = 'tony'

def _reverse(watch_view, **kwargs):
    return reverse('core.views.watch_views.' + watch_view, kwargs=kwargs)

class TestWatchViews(TestCase):
    def setUp(self):
        # Every test needs a client.
        self.user = test_data.createDummyUserRandom(login='johndoe', password='abc123')
        self.client = Client()
        self.client.login(username=self.user.username, password='abc123')

    def test_watch_unwatch_issue(self):
        issue = test_data.create_dummy_issue()
        self.assertTrue(not watch_services.is_watching_issue(self.user, issue.id))

        response = self.client.get(_reverse('watchIssue', issue_id=issue.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, 'WATCHING')
        self.assertTrue(watch_services.is_watching_issue(self.user, issue.id))

        response = self.client.get(_reverse('unwatchIssue', issue_id=issue.id))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, 'NOT_WATCHING')
        self.assertTrue(not watch_services.is_watching_issue(self.user, issue.id))


class TestDeprecatedCoreWatchViews(TestCase):

    def setUp(self):
        self.client = Client()

    def assert_permanent_redirect(self, expected_url, deprecated_url, status_code=301):
        response = self.client.get(deprecated_url)
        location = response._headers['location'][1]
        self.assertTrue(location.endswith(expected_url))
        self.assertEqual(response.status_code, status_code)

    def test_watch_issue(self):
        issue = test_data.create_dummy_issue()
        self.assert_permanent_redirect(_reverse('watchIssue', issue_id=issue.id),
            '/core/watch/issue/%s' % issue.id)

    def test_unwatch_issue(self):
        issue = test_data.create_dummy_issue()
        self.assert_permanent_redirect(_reverse('unwatchIssue', issue_id=issue.id),
            '/core/unwatch/issue/%s' % issue.id)
