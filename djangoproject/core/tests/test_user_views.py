from django.test import TestCase
from helpers import test_data
from django.test.client import Client


class TestRedirectToUser(TestCase):
    def setUp(self):
        self.user = test_data.createDummyUserRandom(login='johndoe', password='abc123')
        self.client = Client()
        self.client.login(username=self.user.username, password='abc123')

    def test_redirect_after_email_activation(self):
        response = self.client.get('/email/')
        self.assertEqual(response.status_code, 302)
        location = response['Location']
        self.assertIn(self.user.get_view_link(), location)
        self.assertIn('email_verified=true', location)


class TestUserUnauthenticatedViews(TestCase):

    def setUp(self):
        self.user = test_data.createDummyUserRandom(login='johndoe', password='abc123')
        self.another_user = test_data.createDummyUserRandom(login='janeroe', password='abc123')
        self.client = Client()

    def test_list_users(self):
        response = self.client.get('/user/')
        self.assertTemplateUsed(response, 'core2/userlist.html')
        self.assertEqual(2, len(response.context['users']))

    def test_view_user(self):
        response = self.client.get('/user/%d/' % self.user.id)
        self.assertTemplateUsed(response, 'core2/user.html')
        self.assertEqual(self.user, response.context['le_user'])

    def test_view_user_with_slug(self):
        response = self.client.get('/user/%d/%s' % (self.user.id, self.user.username))
        self.assertTemplateUsed(response, 'core2/user.html')
        self.assertEqual(self.user, response.context['le_user'])

    def test_view_edit_form(self):
        response = self.client.get('/user/edit', follow=True)
        self.assertTrue(response.redirect_chain)

    def test_view_edit_submit(self):
        response = self.client.post('/user/edit/submit', follow=True)
        self.assertTrue(response.redirect_chain)


class TestUserAuthenticatedViews(TestCase):

    def setUp(self):
        self.user = test_data.createDummyUserRandom(login='johndoe', password='abc123')
        self.another_user = test_data.createDummyUserRandom(login='janeroe', password='abc123')
        self.client = Client()
        self.client.login(username=self.user.username, password='abc123')

    def test_view_edit_form(self):
        response = self.client.get('/user/edit', follow=True)
        self.assertEqual([], response.redirect_chain)

    def test_view_edit_submit(self):
        response = self.client.post('/user/edit/submit', {
            'screenName': 'John Doe',
            'website': 'http://www.test.com',
            'about': 'A placeholder user.',
            'realName': 'John Doe',
            'preferred_language_code': 'en',
            'primaryEmail': 'john@test.com',
            'bitcoin_receive_address': 'null'
        }, follow=True)
        redirect_url = response.redirect_chain[0][0]
        redirect_status = response.redirect_chain[0][1]
        self.assertEqual(302, redirect_status)
        self.assertTrue(redirect_url.startswith('http://testserver/user/'))
        self.assertTrue(redirect_url.endswith('/john-doe?prim=true'))


class TestDeprecatedCoreUserViews(TestCase):

    def setUp(self):
        self.user = test_data.createDummyUserRandom(login='johndoe', password='abc123')
        self.client = Client()
        self.client.login(username=self.user.username, password='abc123')

    def _assert_redirect(self, url):
        response = self.client.get('/core' + url, follow=True)
        expected = [('http://testserver' + url, 301)]
        self.assertEqual(expected, response.redirect_chain)

    def test_list_users(self):
        self._assert_redirect('/user/')

    def test_view_user(self):
        self._assert_redirect('/user/%d/' % self.user.id)

    def test_view_user_with_slug(self):
        self._assert_redirect('/user/%d/%s' % (self.user.id, self.user.username))
