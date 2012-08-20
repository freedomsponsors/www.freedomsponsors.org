from core.models import *
from django.http import HttpResponseRedirect
from django.template import Context, loader, RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.http import HttpResponse
from frespoutils import get_or_none, getUnconnectedSocialAccounts, dictOrEmpty
from django.conf import settings
from emailmgr.models import EmailAddress
from emailmgr import utils as emailmgr_utils
from django.contrib import messages
import logging

def viewUser(request, user_id):
    user = User.objects.get(pk=user_id)
    unconnectedSocialAccounts = None
    changedEmails = None
    if(user.id == request.user.id):
        unconnectedSocialAccounts = getUnconnectedSocialAccounts(user)
    _getAlertsForViewUser(request, user)

    context = {'le_user':user,
        'stats': user.getStats(),
        'unconnectedSocialAccounts':unconnectedSocialAccounts,
        'show_alert' : show_alert,
        }
    if(show_alert):
        context = dict(context.items() + alert_data.items())
    return render_to_response('core/user.html',
        context,
        context_instance = RequestContext(request))
    
def viewUserHistory(request, user_id):
    user = User.objects.get(pk=user_id)
    return render_to_response('core/userhistory.html',
        {'le_user':user,},
        context_instance = RequestContext(request))

@login_required
def editUserForm(request):
    userinfo = request.user.getUserInfo()
    if(not userinfo):
        userinfo = UserInfo.newUserInfo(request.user)
        userinfo.save()
    return render_to_response('core/useredit.html',
        {'userinfo':userinfo,
        'next':dictOrEmpty(request.GET, 'next')},
        context_instance = RequestContext(request))

@login_required
def editUser(request):
    userinfo = request.user.getUserInfo()
    userinfo.screenName = request.POST['screenName']
    userinfo.website = request.POST['website']
    userinfo.about = request.POST['about']
    userinfo.realName = request.POST['realName']
    userinfo.receiveAllEmail = request.POST.has_key('receiveAllEmail')
    userinfo.brazilianPaypal = request.POST.has_key('brazilianPaypal')

    newEmail = request.POST['primaryEmail']
    newPaypalEmail = dictOrEmpty(request.POST, 'paypalEmail')
    if(not newPaypalEmail):
        newPaypalEmail = newEmail

    primaryActivation = _changePrimaryEmailIfNeeded(userinfo, newEmail)
    paypalActivation = _changePaypalEmailIfNeeded(userinfo, newPaypalEmail)

    userinfo.save()
    next = dictOrEmpty(request.POST, 'next')
    if(next):
        return redirect(next)
    else:
        params = []
        if(primaryActivation):
            params.append("prim=true")
        if(paypalActivation):
            params.append("payp=true")
        params = '&'.join(params)
        if(params):
            params = '?'+params
        return redirect(request.user.get_view_link()+params)

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

# TODO: replace this with the message framewor
def _getAlertsForViewUser(request, user):
    if(user.id == request.user.id):
        changedEmails = []
        if (dictOrEmpty(request.GET, 'prim') == 'true'):
            changedEmails.append(user.email)
        if (dictOrEmpty(request.GET, 'payp') == 'true'):
            changedEmails.append(user.getUserInfo().paypalEmail)
        changedEmails = ' and '.join(changedEmails)
        if(changedEmails):
            messages.info(request, "We've sent an email confirmation to "+changedEmails+". Please check you inbox and click the confirmation link to complete email address verification.")
            return

        userinfo = user.getUserInfo()
        if(not (userinfo.is_primary_email_verified and userinfo.is_paypal_email_verified)):
            messages.info(request, "You still have unverified emails. Please check you inbox and click the confirmation link to complete email address verification. To re-send the verification email, just edit and save your profile.")
            return

    if dictOrEmpty(request.GET, 'email_verified') == 'true':
        messages.info(request, "Your email was verified successfully. Thanks ^_^")
        return

    return None, None


def _send_activation(emailActivation):
    emailmgr_utils.send_activation(emailActivation, False)
    emailActivation.is_activation_sent = True
    emailActivation.save()

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

