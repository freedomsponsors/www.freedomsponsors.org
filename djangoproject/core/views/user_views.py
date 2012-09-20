from core.models import *
from django.contrib import messages
from django.template import  RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from core.utils.frespo_utils import  dictOrEmpty
from core.services import user_services

def viewUser(request, user_id):
    user = User.objects.get(pk=user_id)
    unconnectedSocialAccounts = None
    changedEmails = None
    if(user.id == request.user.id):
        unconnectedSocialAccounts = user_services.getUnconnectedSocialAccounts(user)
    alert_strings = user_services.getAlertsForViewUser(request.user, user,
        changedPrimaryEmail=dictOrEmpty(request.GET, 'prim') == 'true',
        changedPaypalEmail=dictOrEmpty(request.GET, 'payp') == 'true',
        emailVerified=dictOrEmpty(request.GET, 'email_verified') == 'true')
    for alert in alert_strings:
        messages.info(request, alert)

    context = {'le_user':user,
        'stats': user.getStats(),
        'unconnectedSocialAccounts':unconnectedSocialAccounts,
        }
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
    paypalActivation, primaryActivation = user_services.edit_existing_user(request.user, request.POST)

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






