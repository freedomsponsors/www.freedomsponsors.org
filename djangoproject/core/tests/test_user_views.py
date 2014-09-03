#coding: utf-8
from unittest.case import skip
from django.contrib.auth.models import User
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
        response = self.client.get('/user/%s/' % self.user.username)
        self.assertTemplateUsed(response, 'core2/user.html')
        self.assertEqual(self.user, response.context['le_user'])

    def test_view_user_with_slug(self):
        response = self.client.get('/user/%d/%s' % (self.user.id, self.user.username), follow=True)
        self.assertTemplateUsed(response, 'core2/user.html')
        self.assertTrue('http://testserver/user/%s/' % self.user.username, response.redirect_chain[-1][0])
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
        self.assertEqual('http://testserver/user/%s?prim=true' % self.user.username, redirect_url)

    def test_change_username_ok(self):
        response = self.client.post('/user/change_username', {
            'new_username': 'oreiudo'
        })
        user = User.objects.get(pk=self.user.id)
        self.assertEqual(200, response.status_code)
        self.assertEqual('oreiudo', user.username)

    def test_change_username_name_already_taken(self):
        old_username = self.user.username
        response = self.client.post('/user/change_username', {
            'new_username': self.another_user.username
        })
        user = User.objects.get(pk=self.user.id)
        self.assertEqual(200, response.status_code)
        self.assertEqual(old_username, user.username)

        msg = [m for m in response.context['messages']][0].message
        self.assertTrue('username is already taken' in msg)

    def test_change_username_name_invalid(self):
        old_username = self.user.username
        response = self.client.post('/user/change_username', {
            'new_username': 'cannót'
        })
        user = User.objects.get(pk=self.user.id)
        self.assertEqual(200, response.status_code)
        self.assertEqual(old_username, user.username)

        msg = [m for m in response.context['messages']][0].message
        self.assertTrue('username is invalid' in msg)

    def test_can_change_username_once_but_not_twice(self):
        response = self.client.post('/user/change_username', {
            'new_username': 'oreiudo'
        })
        self.assertEqual(200, response.status_code)
        user = User.objects.get(pk=self.user.id)
        self.assertEqual('oreiudo', user.username)

        response = self.client.post('/user/change_username', {
            'new_username': 'narigudo'
        })
        user = User.objects.get(pk=self.user.id)
        self.assertEqual(200, response.status_code)
        self.assertEqual('oreiudo', user.username)

        msg = [m for m in response.context['messages']][0].message
        self.assertEqual('You cannot change your username anymore.', msg)


class TestDeprecatedCoreUserViews(TestCase):

    def setUp(self):
        self.user = test_data.createDummyUserRandom(login='johndoe', password='abc123')
        self.client = Client()
        self.client.login(username=self.user.username, password='abc123')

    def _assert_redirect(self, url):
        response = self.client.get('/core' + url, follow=True)
        expected = [('http://testserver' + url, 301)]
        self.assertEqual(expected, response.redirect_chain)

    def _assert_redirect_to_user(self, url):
        response = self.client.get('/core' + url, follow=True)
        self.assertTrue('http://testserver/user/%s/' % self.user.username, response.redirect_chain[-1][0])

    def test_list_users(self):
        self._assert_redirect('/user/')

    def test_view_user(self):
        self._assert_redirect_to_user('/user/%d/' % self.user.id)

    def test_view_user_with_slug(self):
        self._assert_redirect_to_user('/user/%d/%s' % (self.user.id, self.user.username))
