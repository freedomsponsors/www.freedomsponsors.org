import urllib
from core.models import *
from django.contrib import messages
from django.template import  RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from core.utils.frespo_utils import  dictOrEmpty
from django.utils.translation import ugettext as _
from core.services import user_services, mail_services
from django.conf import settings

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

@login_required
def editUserForm(request):
    userinfo = request.user.getUserInfo()
    available_languages = [
        {'code':'en', 'label':_('English')},
        {'code':'pt-br', 'label':_('Brazilian Portuguese')},
        {'code':'es', 'label':_('Spanish')},
    ]
    if(not userinfo):
        userinfo = UserInfo.newUserInfo(request.user)
        userinfo.save()
        mail_services.welcome(request.user)
        _notify_admin_new_user(request.user)
    return render_to_response('core/useredit.html',
        {'userinfo':userinfo,
         'available_languages' : available_languages,
        'next':dictOrEmpty(request.GET, 'next')},
        context_instance = RequestContext(request))

def _notify_admin_new_user(user):
    mail_services.notify_admin(subject=_('New user registered: ')+user.getUserInfo().screenName,
        msg=settings.SITE_HOME+user.get_view_link())

@login_required
def editUser(request):
    paypalActivation, primaryActivation = user_services.edit_existing_user(request.user, request.POST)

    next = dictOrEmpty(request.POST, _('next'))
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

def listUsers(request):
    users = user_services.get_users_list()
    return render_to_response('core/userlist.html',
        {'users':users,},
        context_instance = RequestContext(request))

@login_required
def redirect_to_user_page(request, **kwargs):
    link = request.user.get_view_link()
    if kwargs:
        link += '?' + urllib.urlencode(kwargs)
    return redirect(link)
