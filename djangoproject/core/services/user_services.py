from core.services import paypal_services, mail_services, FSException
from emailmgr import utils as emailmgr_utils
from emailmgr.models import EmailAddress
from core.models import *
from django.conf import settings
import re

__author__ = 'tony'

def getAlertsForViewUser(logged_user, user_to_view, changedPrimaryEmail, changedPaypalEmail, emailVerified):
    if(user_to_view.id == logged_user.id):
        changedEmails = []
        if changedPrimaryEmail:
            changedEmails.append(user_to_view.email)
        if changedPaypalEmail:
            changedEmails.append(user_to_view.getUserInfo().paypalEmail)
        changedEmails = ' and '.join(changedEmails)
        if(changedEmails):
            return ["We've sent an email confirmation to "+changedEmails+". Please check you inbox and click the confirmation link to complete email address verification."]

        userinfo = user_to_view.getUserInfo()
        if(not (userinfo.is_primary_email_verified and userinfo.is_paypal_email_verified)):
            return ["You still have unverified emails. Please check you inbox and click the confirmation link to complete email address verification. To re-send the verification email, just edit and save your profile."]

    if emailVerified:
        return ["Your email was verified successfully. Thanks ^_^"]

    return None, None


def edit_existing_user(user, dict):
    userinfo = user.getUserInfo()
    new_username = dict.get('username')
    if new_username and not is_valid_username(new_username):
        raise FSException('Invalid username (must not contain any special characters')
    first_time = userinfo.date_last_updated == userinfo.date_created
    if first_time:
        new_username = dict['username']
        if new_username != user.username:
            change_username(user, new_username)
    now = timezone.now()
    userinfo.website = dict['website']
    userinfo.about = dict['about']
    userinfo.realName = dict['realName']
    userinfo.receiveEmail_issue_comments = dict.has_key('receiveEmail_issue_comments')
    userinfo.receiveEmail_issue_work = dict.has_key('receiveEmail_issue_work')
    userinfo.receiveEmail_issue_offer = dict.has_key('receiveEmail_issue_offer')
    userinfo.receiveEmail_issue_payment = dict.has_key('receiveEmail_issue_payment')
    userinfo.receiveEmail_announcements = dict.has_key('receiveEmail_announcements')
    userinfo.brazilianPaypal = dict.has_key('brazilianPaypal')
    userinfo.hide_from_userlist = dict.has_key('hide_from_userlist')
    userinfo.preferred_language_code = dict['preferred_language_code']
    userinfo.date_last_updated = now
    if settings.BITCOIN_ENABLED:
        userinfo.bitcoin_receive_address = dict['bitcoin_receive_address']
    newEmail = dict['primaryEmail']
    newPaypalEmail = dict.get('paypalEmail')
    if not newPaypalEmail:
        newPaypalEmail = newEmail
    changedPaypalEmail = newPaypalEmail != userinfo.paypalEmail
    primaryActivation = _changePrimaryEmailIfNeeded(userinfo, newEmail)
    paypalActivation = _changePaypalEmailIfNeeded(userinfo, newPaypalEmail)
    if changedPaypalEmail:
        userinfo.paypal_verified = False
    userinfo.save()
    paypal_services.accepts_paypal_payments(user)
    return paypalActivation, primaryActivation


def deactivate_user(user):
    for solution in Solution.objects.filter(programmer=user, status=Solution.IN_PROGRESS):
        solution.abort()
    for offer in Offer.objects.filter(sponsor=user, status=Offer.OPEN):
        offer.revoke()
    Watch.objects.filter(user=user).delete()
    user.is_active = False
    user.save()
    mail_services.deactivated(user)
    subject = 'user deactivated: %s/%s' % (user.id, user.username)
    body = '<a href="http://freedomsponsors.org/user/%s">%s</a>' % (user.id, user.username)
    mail_services.notify_admin(subject, body)


def is_valid_username(username):
    return re.search(r'^[\w\-_]*[a-zA-Z][\w\-_]*$', username) is not None


def is_username_available(username):
    existing_user = get_or_none(User, username=username)
    return False if existing_user else True


def change_username(user, new_username):
    can_change = user.getUserInfo().can_change_username
    if not can_change:
        raise FSException('You cannot change your username anymore.')
    if not is_valid_username(new_username):
        raise FSException('Sorry, this username is invalid.')
    if not is_username_available(new_username):
        raise FSException('Sorry, that username is already taken.')
    old_username = user.username
    user.username = new_username
    user.save()
    userinfo = user.getUserInfo()
    userinfo.can_change_username = False
    userinfo.save()
    subject = 'user %s changed username %s --> %s' % (user.id, old_username, new_username)
    body = '<a href="http://freedomsponsors.org/user/%s">%s</a>' % (user.id, new_username)
    mail_services.notify_admin(subject, body)


def get_users_list():
    return UserInfo.objects.filter(hide_from_userlist = False).order_by("-id")


def _changePaypalEmailIfNeeded(userinfo, newPaypalEmail):
    oldPaypalEmail = userinfo.paypalEmail
    if newPaypalEmail != oldPaypalEmail:
        userinfo.paypalEmail = newPaypalEmail
    do_it = newPaypalEmail != userinfo.user.email and (
        newPaypalEmail != oldPaypalEmail or
        not userinfo.is_paypal_email_verified)
    if do_it:
        emailActivation = _makeEmailActivation(userinfo.user, newPaypalEmail, 'PAYPAL')
        _send_activation(emailActivation)
        userinfo.is_paypal_email_verified = False
        return True
    return False


def _changePrimaryEmailIfNeeded(userinfo, newEmail):
    user = userinfo.user
    if(user.email != newEmail):
        emailActivation = _makeEmailActivation(user, newEmail, 'PRIMARY')
        _send_activation(emailActivation)
        user.email = newEmail
        user.save()
        userinfo.is_primary_email_verified = False
        return True
    if(not userinfo.is_primary_email_verified):
        emailActivation = _makeEmailActivation(user, user.email, 'PRIMARY')
        _send_activation(emailActivation)
        return True
    return False


def _makeEmailActivation(user, email, type):
    emailActivations = EmailAddress.objects.filter(user__id=user.id, email=email)
    if(emailActivations.count() > 0):
        emailActivation = emailActivations[0]
    else:
        emailActivation = EmailAddress()
        emailActivation.user = user
        emailActivation.email = email
    emailActivation.is_primary = type == 'PRIMARY'
    emailActivation.is_activation_sent = False
    emailActivation.save()
    return emailActivation


def _send_activation(emailActivation):
    emailmgr_utils.send_activation(emailActivation, False)
    emailActivation.is_activation_sent = True
    emailActivation.save()