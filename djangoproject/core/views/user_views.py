import urllib
from django.http import HttpResponse
from core.models import *
from django.contrib import messages
from django.template import  RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from django.utils.translation import ugettext as _
from core.services import user_services, mail_services, FSException
from django.conf import settings


def viewUserById(request, user_id, user_slug=None):
    try:
        user = User.objects.get(pk=user_id)
    except:
        return HttpResponse(status=404, content='User not found')

    return redirect('/user/%s' % user.username, permanent=True)


def viewUserByUsername(request, username):
    try:
        user = User.objects.get(username=username)
    except:
        return HttpResponse(status=404, content='User not found')

    if not user.is_active and not request.user.is_superuser:
        return render_to_response(
            'core2/user_inactive.html',
            {'le_user': user},
            context_instance=RequestContext(request)
        )
    unconnectedSocialAccounts = None
    if user.id == request.user.id:
        unconnectedSocialAccounts = user.getUnconnectedSocialAccounts()
    alert_strings = user_services.getAlertsForViewUser(
        request.user, user,
        changedPrimaryEmail=request.GET.get('prim') == 'true',
        changedPaypalEmail=request.GET.get('payp') == 'true',
        emailVerified=request.GET.get('email_verified') == 'true'
    )
    for alert in alert_strings:
        messages.info(request, alert)
    context = {
        'le_user': user,
        'stats': user.getStats(),
        'unconnectedSocialAccounts': unconnectedSocialAccounts,
    }
    return render_to_response(
        'core2/user.html',
        context,
        context_instance=RequestContext(request)
    )


@login_required
def editUserForm(request):
    userinfo = request.user.getUserInfo()
    available_languages = [
        {'code': 'en', 'label': _('English')},
        {'code': 'pt-br', 'label': _('Brazilian Portuguese')},
        {'code': 'es', 'label': _('Spanish')},
    ]
    if not userinfo:
        userinfo = UserInfo.newUserInfo(request.user)
        userinfo.save()
        mail_services.welcome(request.user)
        _notify_admin_new_user(request.user)
    first_time = userinfo.date_last_updated == userinfo.date_created

    return render_to_response('core2/useredit.html', {
        'userinfo': userinfo,
        'can_edit_username': first_time,
        'available_languages': available_languages,
        'next': request.GET.get('next', '')},
        context_instance=RequestContext(request)
    )


def _notify_admin_new_user(user):
    mail_services.notify_admin(subject=_('New user registered: ')+user.username,
                               msg=settings.SITE_HOME+user.get_view_link())


@login_required
def editUser(request):
    try:
        paypalActivation, primaryActivation = user_services.edit_existing_user(request.user, request.POST)
    except FSException as e:
        messages.error(request, e.message)
        return redirect('/user/edit')

    next = request.POST.get(_('next'))
    if next:
        return redirect(next)
    else:
        params = []
        if primaryActivation:
            params.append("prim=true")
        if paypalActivation:
            params.append("payp=true")
        params = '&'.join(params)
        if params:
            params = '?'+params
        return redirect(request.user.get_view_link()+params)


def listUsers(request):
    users = user_services.get_users_list()
    return render_to_response(
        'core2/userlist.html',
        {'users': users},
        context_instance=RequestContext(request)
    )


@login_required
def redirect_to_user_page(request, **kwargs):
    link = request.user.get_view_link()
    if kwargs:
        link += '?' + urllib.urlencode(kwargs)
    return redirect(link)


@login_required
def cancel_account(request):
    user_services.deactivate_user(request.user)
    messages.info(request, 'Your account has been disabled.')
    return redirect('/logout')


@login_required
def change_username(request):
    can_change = request.user.getUserInfo().can_change_username
    if request.method.lower() == 'post':
        new_username = request.POST['new_username']
        try:
            user_services.change_username(request.user, new_username)
            messages.info(request, 'Your username has been changed')
        except FSException as e:
            messages.error(request, e.message)
    return render_to_response(
        'core2/change_username.html',
        {'can_change': can_change},
        context_instance=RequestContext(request)
    )
