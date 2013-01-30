from core.utils.frespo_utils import socialImages, dictOrEmpty
from emailmgr import utils as emailmgr_utils
from emailmgr.models import EmailAddress
from django.contrib.auth.models import User
from core.models import *

__author__ = 'tony'

def getUnconnectedSocialAccounts(user):
    imgs = socialImages.copy()
    for auth in user.getSocialAuths():
        if imgs.has_key(auth.provider):
            del imgs[auth.provider]
    res = []
    for provider in imgs.keys():
        res.append({'provider':provider, 'icon':imgs[provider]})
    return res


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
            return "You still have unverified emails. Please check you inbox and click the confirmation link to complete email address verification. To re-send the verification email, just edit and save your profile."

    if emailVerified:
        return "Your email was verified successfully. Thanks ^_^"

    return None, None


def edit_existing_user(user, dict):
    userinfo = user.getUserInfo()
    userinfo.screenName = dict['screenName']
    userinfo.website = dict['website']
    userinfo.about = dict['about']
    userinfo.realName = dict['realName']
    userinfo.receiveAllEmail = dict.has_key('receiveAllEmail')
    userinfo.brazilianPaypal = dict.has_key('brazilianPaypal')
    userinfo.hide_from_userlist = dict.has_key('hide_from_userlist')
    userinfo.preferred_language_code = dict['preferred_language_code']
    newEmail = dict['primaryEmail']
    newPaypalEmail = dictOrEmpty(dict, 'paypalEmail')
    if(not newPaypalEmail):
        newPaypalEmail = newEmail
    primaryActivation = _changePrimaryEmailIfNeeded(userinfo, newEmail)
    paypalActivation = _changePaypalEmailIfNeeded(userinfo, newPaypalEmail)
    userinfo.save()
    return paypalActivation, primaryActivation

def get_users_list():
    return UserInfo.objects.filter(hide_from_userlist = False).order_by("-id")


def _changePaypalEmailIfNeeded(userinfo, newPaypalEmail):
    oldPaypalEmail = userinfo.paypalEmail
    if(newPaypalEmail != userinfo.paypalEmail):
        userinfo.paypalEmail = newPaypalEmail
    do_it = newPaypalEmail != userinfo.user.email and (
        newPaypalEmail != oldPaypalEmail or
        not userinfo.is_paypal_email_verified)
    if(do_it):
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