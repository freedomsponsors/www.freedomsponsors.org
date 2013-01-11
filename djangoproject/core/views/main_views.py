# coding: utf-8
from django.http import HttpResponseRedirect
from django.contrib.auth import logout as auth_logout
from django.template import  RequestContext
from django.shortcuts import render_to_response, redirect
from core.services import issue_services
from core.utils.frespo_utils import  dictOrEmpty
from core.services.mail_services import *
from core.services import stats_services
from core.models import Issue
from django.contrib import messages
import logging

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
    if(request.user.is_superuser):
        mail_to = dictOrEmpty(request.POST, 'mail_to')
        if(mail_to):
            subject = dictOrEmpty(request.POST, 'subject')
            body = dictOrEmpty(request.POST, 'body')
            if(mail_to == 'some'):
                emails = dictOrEmpty(request.POST, 'emails').split(',')
                count = 0
                for email in emails:
                    plain_send_mail(email.strip(), subject, body)
                    count += 1
            elif(mail_to == 'all'):
                count = send_mail_to_all_users(subject, body)
            messages.info(request, 'mail sent to %s users'%count)
    else:
        messages.info(request, 'nice try :-). If you do find a hole, please have the finesse to let us know though.')
    return render_to_response('core/admail.html',
        {},
        context_instance = RequestContext(request))

def home(request):
    context = RequestContext(request, {
        'issues_sponsoring': Issue.sponsoring.recently_updated()[0:10],
        'issues_kickstarting': Issue.kickstarting.recently_updated()[0:10]
    })
    return render_to_response('core/home.html', context_instance=context)


def stats(request):
    stats = stats_services.get_stats()
    return render_to_response('core/stats.html',
        {'stats':stats,},
        context_instance = RequestContext(request))
