# Create your views here.

from django.http import HttpResponseRedirect
from django.contrib.auth import logout as auth_logout
from django.template import  RequestContext
from django.shortcuts import render_to_response, redirect
from core.services import issue_services
from core.services.mail_services import *
from core.services import stats_services
from django.contrib import messages
import logging
from core.services import testmail_service

logger = logging.getLogger(__name__)



def logout(request):
    """Logs out user"""
    auth_logout(request)
    return HttpResponseRedirect('/')
    
def login(request):
    getparams = ''
    if request.GET.has_key('next') : 
        getparams = '?next='+request.GET['next'];
    if request.user.is_authenticated():
        if getparams:
            return redirect(getparams)
        else:
            return redirect('/')
    return render_to_response('core/login.html',
        {'getparams':getparams},
        context_instance = RequestContext(request))


def admail(request):
    if request.user.is_superuser:
        mail_to = request.POST.get('mail_to')
        if mail_to:
            subject = request.POST.get('subject', '')
            body = request.POST.get('body', '')
            if mail_to == 'some':
                emails = request.POST.get('emails', '').split(',')
                count = 0
                for email in emails:
                    plain_send_mail(email.strip(), subject, body, settings.ADMAIL_FROM_EMAIL)
                    count += 1
            elif mail_to == 'all':
                count = send_mail_to_all_users(subject, body, settings.ADMAIL_FROM_EMAIL)
            messages.info(request, 'mail sent to %s users' % count)
    else:
        messages.info(request, 'nice try :-). If you do find a hole, please have the finesse to let us know though.')
    return render_to_response('core/admail.html',
                              {},
                              context_instance = RequestContext(request))


def mailtest(request):
    to = ''
    if request.user.is_superuser:
        to = request.POST.get('to')
        test = request.POST.get('test')
        if test:
            testmail_service.mailtest(test, to)
            msg = 'test mail %s sent to %s.' % (test, to)
            messages.info(request, msg)
    else:
        messages.info(request, 'nice try :-). If you do find a hole, please have the finesse to let us know though.')
    return render_to_response('core/mailtest.html',
                              {'to': to},
                              context_instance = RequestContext(request))


def home(request):
    if(request.user.is_authenticated() and request.user.getUserInfo() == None):
        return redirect('/core/user/edit')
    issues_sponsoring = issue_services.search_issues(is_public_suggestion = False)[0:20]
    issues_kickstarting = issue_services.search_issues(is_public_suggestion = True)[0:20]
    return render_to_response('core/home.html',
        {'issues_sponsoring':issues_sponsoring,
         'issues_kickstarting':issues_kickstarting},
        context_instance = RequestContext(request))


def stats(request):
    stats = stats_services.get_stats()
    return render_to_response('core/stats.html',
        {'stats':stats,},
        context_instance = RequestContext(request))








