# -*- coding: utf-8 -*-
"""Unit tests for django emailmgr"""
from django.conf import settings
from django.test import TestCase
from django.template import Context, Template
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from emailmgr.models import EmailAddress
from django.test.client import Client
from django.core.urlresolvers import reverse
from emailmgr import forms
from django.contrib.auth import authenticate


############################################
class EmailUniquenessTestCase(TestCase):
    """Tests for Django emailmgr - Uniqueness """
    def setUp(self):
        self.client = Client()

        #create a base test user
        self.user = User.objects.create_user('unique', 'unique@example.com', '1pass')
        
    def test_email_address_uniqueness(self):
        """
        Test & validates email addresses uniqueness
        """
        # create a user with an email address first
        user = User.objects.create_user('mike', 'mike@example.com', '2secret')

        # test against User.email
        # test a unique email address
        form = forms.EmailAddressForm(user=user, data={'email': 'john@example.com'})
        self.failUnless(form.is_valid())

        # test a duplicated email address
        form = forms.EmailAddressForm(user=user, data={'email': 'mike@example.com'})
        self.failIf(form.is_valid())
        self.assertEqual(form.errors['email'],[u"This email address already in use."])

        # test against EmailAddress.email
        email = EmailAddress(**{'user': user, 'email': 'alvin@example.com'})
        email.save()
        
        # test a duplicated email address
        form = forms.EmailAddressForm(user=user, data={'email': 'alvin@example.com'})
        self.failIf(form.is_valid())
        self.assertEqual(form.errors['email'],[u"This email address already in use."])

        # test a unique email address
        form = forms.EmailAddressForm(user=user, data={'email': 'sam@example.com'})
        self.failUnless(form.is_valid())


############################################
class EmailAutoCreationBySignalsTestCase(TestCase):
    """Tests for Django emailmgr -- Create by singals """
    def setUp(self):
        #create a base test user
        self.user = User.objects.create_user('autocreate', 'autocreate@example.com', '1pass')
        
    def test_email_add_by_signals(self):
        # check that the first email address was already created by User creation signals
        e = EmailAddress.objects.all()
        self.failUnless(len(e)==1)
        self.failUnless(e[0].email=='autocreate@example.com')
        self.failUnless(e[0].is_primary)
        self.failUnless(e[0].is_active)

############################################
class EmailAutoDeletionBySignalsTestCase(TestCase):
    """Tests for Django emailmgr -- Delete by singals """
        
    def test_email_add_by_signals(self):
        #import pdb; pdb.set_trace()
        u = User.objects.create_user('dumpall', 'dumpall@example.com', '1pass')

        # check that email address was created for testdelete user
        e = EmailAddress.objects.all()
        self.failUnless(len(e)==1)
        self.failUnless(e[0].email=='dumpall@example.com')
        self.failUnless(e[0].is_primary)
        self.failUnless(e[0].is_active)

        # delete the user and make sure all his emails are gone too
        u.delete()
        e = EmailAddress.objects.filter(user=u)
        self.failIf(e)


############################################
class EmailAddTestCase(TestCase):
    """Tests for Django emailmgr -- Add Email """
    def setUp(self):
        #create a base test user
        self.user = User.objects.create_user('add', 'add@example.com', '1pass')
        
    def test_email_add(self):
        #import pdb; pdb.set_trace()
        retval = self.client.login(username='add', password='1pass')
        self.failUnless(retval)
        
        args = {'email': 'add1@example.com'}
        response = self.client.post(reverse('emailmgr_email_add'), args)
        self.assertContains(response, "email address added", status_code=200)

        # make sure the email is saved
        e = EmailAddress.objects.get(email='add1@example.com')
        self.failUnless(e)

        # ensure duplicate email address are rejected
        args = {'email': 'add1@example.com', 'follow': True}
        response = self.client.post(reverse('emailmgr_email_add'), args)        
        self.assertContains(response, "This email address already in use.", status_code=200)
        
        # ensure multiple emails per user are accepted
        args = {'email': 'add2@example.com', 'follow': True}
        response = self.client.post(reverse('emailmgr_email_add'), args)        
        self.assertNotContains(response, "This email address already in use.", status_code=200)
        
        # make sure the new email is in our database
        e = EmailAddress.objects.get(email='add2@example.com')
        self.failUnless(e)
        self.failIf(e.is_primary)
        self.failUnless(e.identifier)

        # make sure we have 3 emails for this user
        e = EmailAddress.objects.all()
        self.failUnless(len(e)==3)

        user = User.objects.create_user('add3', 'add3@example.com', '1pass')

        # make sure we have 4 emails total
        e = EmailAddress.objects.all()
        self.failUnless(len(e)==4)
        
        e = EmailAddress.objects.get(email='add3@example.com')
        self.failUnless(e)
        self.failUnless(e.is_primary)
        self.failUnless(e.is_active)
        self.failUnless(e.identifier)
        
        e1 = EmailAddress.objects.get(user=user)
        self.failUnless(e==e1)

class EmailListTestCase(TestCase):
    """Tests for Django emailmgr -- Add Email """
    def setUp(self):
        #create a base test user
        self.user = User.objects.create_user('list', 'list@example.com', '1pass')
        
    def test_email_list(self):
        # establish a session
        retval = self.client.login(username='list', password='1pass')
        self.failUnless(retval)

        # add few emails to user
        args = {'email': 'list1@example.com', 'follow': True}
        response = self.client.post(reverse('emailmgr_email_add'), args) 
        self.assertNotContains(response, "This email address already in use.", status_code=200)

        args = {'email': 'list2@example.com', 'follow': True}
        response = self.client.post(reverse('emailmgr_email_add'), args)        
        self.assertNotContains(response, "This email address already in use.", status_code=200)

        # verify that all emails were added, 2 added by us and 1 by user creation
        e = EmailAddress.objects.all()
        self.failUnless(len(e)==3)

        # list all email addresses
        response = self.client.post(reverse('emailmgr_email_list'))        
        self.assertNotContains(response, "This email address already in use.", status_code=200)
        self.assertContains(response, "example.com", count=3, status_code=200)
        self.assertContains(response, "Send Activation", count=2, status_code=200)

        # make sure the option of adding new email is pased in to template
        self.assertContains(response, "id_email", count=2, status_code=200)


class EmailDeleteTestCase(TestCase):
    """Tests for Django emailmgr -- Add Email """
    def setUp(self):
        #create a base test user
        self.user = User.objects.create_user('delete', 'delete@example.com', '1pass')
        
    def test_email_delete(self):
        # establish a session
        retval = self.client.login(username='delete', password='1pass')
        self.failUnless(retval)
        
        # add few emails to user
        args = {'email': 'delete1@example.com', 'follow': True}
        response = self.client.post(reverse('emailmgr_email_add'), args) 
        self.assertNotContains(response, "This email address already in use.", status_code=200)

        args = {'email': 'delete2@example.com', 'follow': True}
        response = self.client.post(reverse('emailmgr_email_add'), args)        
        self.assertNotContains(response, "This email address already in use.", status_code=200)

        # verify that all emails were added, 2 by us, 1 by user creation
        e = EmailAddress.objects.all()
        self.failUnless(len(e)==3)

        # delete the first email, this is the primary email address, cannot remove
        path = reverse('emailmgr_email_delete', kwargs={'identifier': e[0].identifier})
        response = self.client.get(path, follow=True)        
        self.assertContains(response, "cannot remove primary email address", count=1, status_code=200)
        self.assertContains(response, "example.com", count=3, status_code=200)
        self.assertContains(response, "Send Activation", count=2, status_code=200)
        
        # delete the second email,
        path = reverse('emailmgr_email_delete', kwargs={'identifier': e[1].identifier})
        response = self.client.get(path, follow=True)        
        self.assertNotContains(response, "cannot remove primary email address", status_code=200)
        self.assertContains(response, "email address removed", count=1, status_code=200)
        self.assertContains(response, "example.com", count=2, status_code=200)
        self.assertContains(response, "Send Activation", count=1, status_code=200)       

        # delete the second email again
        path = reverse('emailmgr_email_delete', kwargs={'identifier': e[1].identifier})
        response = self.client.get(path, follow=True)     
        self.failUnless(response.status_code == 404)   
            
        #delete the third email,
        path = reverse('emailmgr_email_delete', kwargs={'identifier': e[2].identifier})
        response = self.client.get(path, follow=True)        
        self.assertNotContains(response, "cannot remove primary email address", status_code=200)
        self.assertContains(response, "email address removed", count=1, status_code=200)
        self.assertContains(response, "example.com", count=1, status_code=200)
        self.assertContains(response, "Primary Email", count=1, status_code=200)
        self.assertNotContains(response, "Make Primary", status_code=200)
        self.assertNotContains(response, "Send Activation", status_code=200)       
    

class EmailActivateTestCase(TestCase):
    """Tests for Django emailmgr -- Activate Email """
    def setUp(self):
        #create a base test user
        self.user = User.objects.create_user('activate', 'activate@example.com', '1pass')
        
    def test_email_activate(self):
        # establish a session
        retval = self.client.login(username='activate', password='1pass')
        self.failUnless(retval)

        # add few emails to user
        args = {'email': 'activate1@example.com', 'follow': True}
        response = self.client.post(reverse('emailmgr_email_add'), args) 
        self.assertNotContains(response, "This email address already in use.", status_code=200)

        args = {'email': 'activate2@example.com', 'follow': True}
        response = self.client.post(reverse('emailmgr_email_add'), args)        
        self.assertNotContains(response, "This email address already in use.", status_code=200)

        # verify that all emails were added, 2 by us, 1 by user creation
        e = EmailAddress.objects.all()
        self.failUnless(len(e)==3)

        # send activation email for the second email that is not primary
        path = reverse('emailmgr_email_send_activation', kwargs={'identifier': e[1].identifier})
        response = self.client.get(path, follow=True)        
        self.assertContains(response, "example.com", count=3, status_code=200)
        self.assertContains(response, "Send Activation", count=1, status_code=200)
        self.assertContains(response, "Resend Activation", count=1, status_code=200)
        self.assertContains(response, "activation email sent", count=1, status_code=200)
        
        # email is out, but pretent we have the email, so activate the second email
        path = reverse('emailmgr_email_activate', kwargs={'identifier': e[1].identifier})
        response = self.client.get(path, follow=True)        
        self.assertContains(response, "example.com", count=3, status_code=200)
        self.assertContains(response, "Send Activation", count=1, status_code=200)
        self.assertContains(response, "email address is now active", count=1, status_code=200)

        e = EmailAddress.objects.get(identifier__iexact=e[1].identifier)
        self.failUnless(e.is_active)

class EmailMakePrimaryTestCase(TestCase):
    """Tests for Django emailmgr -- Make Primary """
    def setUp(self):
        #create a base test user
        self.user = User.objects.create_user('primary', 'primary@example.com', '1pass')
        
    def test_email_activate(self):
        # establish a session
        retval = self.client.login(username='primary', password='1pass')
        self.failUnless(retval)

        # add few emails to user
        args = {'email': 'primary1@example.com', 'follow': True}
        response = self.client.post(reverse('emailmgr_email_add'), args) 
        self.assertNotContains(response, "This email address already in use.", status_code=200)

        args = {'email': 'primary2@example.com', 'follow': True}
        response = self.client.post(reverse('emailmgr_email_add'), args)        
        self.assertNotContains(response, "This email address already in use.", status_code=200)

        # verify that all emails were added, 2 by us, 1 by user creation
        e = EmailAddress.objects.all()
        self.failUnless(len(e)==3)

        # try to make the already primary email primary
        path = reverse('emailmgr_email_make_primary', kwargs={'identifier': e[0].identifier})
        response = self.client.get(path, follow=True)        
        self.assertContains(response, "example.com", count=3, status_code=200)
        self.assertContains(response, "Send Activation", count=2, status_code=200)
        self.assertContains(response, "Primary Email", count=1, status_code=200)
        self.assertContains(response, "email address is already primary", count=1, status_code=200)

        # now try to make the second email that is not activated yet the primary email
        path = reverse('emailmgr_email_make_primary', kwargs={'identifier': e[1].identifier})
        response = self.client.get(path, follow=True)        
        self.assertContains(response, "example.com", count=3, status_code=200)
        self.assertContains(response, "Send Activation", count=2, status_code=200)
        self.assertContains(response, "Primary Email", count=1, status_code=200)
        self.assertNotContains(response, "Make Primary", status_code=200)
        self.assertContains(response, "email address must be activated first", count=1, status_code=200)

        # ok, send activation email for the second email address that is not primary
        path = reverse('emailmgr_email_send_activation', kwargs={'identifier': e[1].identifier})
        response = self.client.get(path, follow=True)        
        self.assertContains(response, "example.com", count=3, status_code=200)
        self.assertContains(response, "Send Activation", count=1, status_code=200)
        self.assertContains(response, "Resend Activation", count=1, status_code=200)
        self.assertContains(response, "activation email sent", count=1, status_code=200)
        
        # email is out, but pretent we have the email, so activate the second email
        path = reverse('emailmgr_email_activate', kwargs={'identifier': e[1].identifier})
        response = self.client.get(path, follow=True)        
        self.assertContains(response, "example.com", count=3, status_code=200)
        self.assertContains(response, "Send Activation", count=1, status_code=200)
        self.assertNotContains(response, "Resend Activation", status_code=200)
        self.assertContains(response, "email address is now active", count=1, status_code=200)

        email = EmailAddress.objects.get(identifier__iexact=e[1].identifier)
        self.failUnless(email.is_active)

        # ok, the second email is activated, now make it primary
        path = reverse('emailmgr_email_make_primary', kwargs={'identifier': e[1].identifier})
        response = self.client.get(path, follow=True)        
        self.assertContains(response, "example.com", count=3, status_code=200)
        self.assertContains(response, "Send Activation", count=1, status_code=200)
        self.assertContains(response, "Primary Email", count=1, status_code=200)
        self.assertContains(response, "Make Primary", count=1, status_code=200)
        self.assertContains(response, "primary address changed", count=1, status_code=200)

        email = EmailAddress.objects.get(identifier__iexact=e[1].identifier)
        self.failUnless(email.is_active)
        self.failUnless(email.is_primary)
        self.failUnless(email.email==email.user.email)



