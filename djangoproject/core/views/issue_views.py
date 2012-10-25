from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from core.utils.frespo_utils import get_or_none, dictOrEmpty, twoplaces
from core.models import *
from core.services import issue_services, watch_services, payment_services
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)

__author__ = 'tony'

@login_required
def addIssue(request):
    try:
        offer = issue_services.sponsor_new_issue(request.POST, request.user)
        watch_services.watch_issue(request.user, offer.issue.id, IssueWatch.SPONSORED)
    except BaseException as ex:
        return HttpResponse("ERROR: "+ex.message)
    params = '?alert=SPONSOR'
    if(dictOrEmpty(request.POST, 'invoke_parent_callback') == 'true'):
        params += '&c=s' # c = Callback (iframe javascript callback)

    return redirect(offer.get_view_link()+params)

@login_required
def kickstartIssue(request):
    try:
        issue = issue_services.kickstart_new_issue(request.POST, request.user)
        watch_services.watch_issue(request.user, issue.id, IssueWatch.CREATED)
    except BaseException as ex:
        return HttpResponse("ERROR: "+ex.message)

    params= '?alert=KICKSTART'
    return redirect(issue.get_view_link()+params)


@login_required
def abortSolution(request):
    solution_id = int(request.POST['solution_id'])
    comment_content = request.POST['comment']
    solution = issue_services.abort_existing_solution(solution_id, comment_content, request.user)
    return redirect(solution.issue.get_view_link())


@login_required
def addSolution(request):
    """Start working on this issue"""
    issue_id = int(request.POST['issue_id'])
    comment_content = request.POST['comment']
    issue = issue_services.add_solution_to_existing_issue(issue_id, comment_content, request.user)
    watch_services.watch_issue(request.user, issue.id, IssueWatch.STARTED_WORKING)
    return redirect(issue.get_view_link())


@login_required
def editOffer(request):
    offer_id = int(request.POST['offer_id'])
    offer = issue_services.change_existing_offer(offer_id, request.POST, request.user)
    return redirect(offer.get_view_link())


def listIssues(request):
    project_id = request.GET.get('project_id')
    project_name = request.GET.get('project_name')
    search_terms = request.GET.get('s')
    operation = dictOrEmpty(request.GET, 'operation')
    is_public_suggestion = None
    if(operation == 'SPONSOR'):
        is_public_suggestion = False
    elif(operation == 'KICKSTART'):
        is_public_suggestion = True
    issues = issue_services.search_issues(project_id, project_name, search_terms, is_public_suggestion)
    return render_to_response('core/issue_list.html',
        {'issues':issues,
         's':search_terms,
         'project_id':project_id,
         'project_name':project_name,
         'operation':operation,
        },
        context_instance = RequestContext(request))


@login_required
def myissues(request):
    if(request.user.is_authenticated() and request.user.getUserInfo() == None):
        return redirect('/core/user/edit')
    return render_to_response('core/myissues.html',
        {},
        context_instance = RequestContext(request))


@login_required
def resolveSolution(request):
    solution_id = int(request.POST['solution_id'])
    comment_content = request.POST['comment']
    solution = issue_services.resolve_existing_solution(solution_id, comment_content, request.user)
    return redirect(solution.issue.get_view_link())


@login_required
def revokeOffer(request):
    offer_id = int(request.POST['offer_id'])
    comment_content = request.POST['comment']

    offer = issue_services.revoke_existing_offer(offer_id, comment_content, request.user)

    return redirect(offer.issue.get_view_link())


@login_required
def sponsorIssue(request):
    issue_id = int(request.POST['issue_id'])

    offer = issue_services.sponsor_existing_issue(issue_id, request.POST, request.user)
    watch_services.watch_issue(request.user, issue_id, IssueWatch.SPONSORED)

    invoke_parent_callback = dictOrEmpty(request.POST, 'invoke_parent_callback')
    if(invoke_parent_callback == 'true'):
        params = '?c=s' # c = Callback (iframe javascript callback)
    else:
        params = '?alert=SPONSOR' # a = Alert
    return redirect(offer.get_view_link()+params)


def viewIssue(request, issue_id):
    issue = Issue.objects.get(pk=issue_id)
    myoffer = None
    mysolution = None
    show_alert = None

    if(request.user.is_authenticated()):
        myoffer = get_or_none(Offer, issue=issue,sponsor=request.user)
        mysolution = get_or_none(Solution, issue=issue,programmer=request.user)

    show_sponsor_popup = (dictOrEmpty(request.GET, 'show_sponsor') == 'true')
    alert = dictOrEmpty(request.GET, 'alert')
    if(alert == 'KICKSTART'):
        show_alert = 'core/popup_just_kickstarted.html'
    invoke_parent_callback = (dictOrEmpty(request.GET, 'c') == 's')

    is_watching = request.user.is_authenticated() and watch_services.is_watching_issue(request.user, issue.id)

    return render_to_response('core/issue.html',
        {'issue':issue,
        'is_watching':is_watching,
        'myoffer':myoffer,
        'mysolution':mysolution,
        'invoke_parent_callback' : invoke_parent_callback,
        'show_sponsor_popup' : show_sponsor_popup,
        'show_alert' : show_alert},

        context_instance = RequestContext(request))


def viewOffer(request, offer_id):
    offer = Offer.objects.get(pk=offer_id)
    myoffer = None
    mysolution = None
    show_alert = None

    if(request.user.is_authenticated()):
        mysolution = get_or_none(Solution, issue=offer.issue,programmer=request.user)
        myoffer = get_or_none(Offer, issue=offer.issue,sponsor=request.user)

    alert = dictOrEmpty(request.GET, 'alert')
    if(alert == 'SPONSOR' and offer.issue.project):
        show_alert = 'core/popup_just_sponsored.html'
    invoke_parent_callback = (dictOrEmpty(request.GET, 'c') == 's')

    is_watching = request.user.is_authenticated() and watch_services.is_watching_offer(request.user, offer.id)

    return render_to_response('core/offer.html',
        {'offer':offer,
        'is_watching':is_watching,
        'issue':offer.issue,
        'show_alert':show_alert,
        'myoffer':myoffer,
        'mysolution':mysolution,
        'invoke_parent_callback' : invoke_parent_callback},
        context_instance = RequestContext(request))


@login_required
def addIssueForm(request):
    trackerURL = dictOrEmpty(request.GET, 'trackerURL')
    operation = dictOrEmpty(request.GET, 'operation')
    if(trackerURL):
        issues = Issue.objects.filter(trackerURL__iexact=trackerURL)
        issue_already_exists = issues.count() >= 1
        if(issues.count() > 1):
            logger.warning("Database inconsistency: more than one issue found with url = %s"%trackerURL)
        if(issue_already_exists):
            return redirect(issues[0].get_view_link()+'?show_sponsor=true&c=s')

    return render_to_response('core/add_issue.html',
        {'trackerURL' : trackerURL,
        'operation' : operation},
        context_instance = RequestContext(request))


def listProjects(request):
    projects = Project.objects.all()
    projects = projects.order_by('name')
    return render_to_response('core/project_list.html',
        {'projects':projects},
        context_instance = RequestContext(request))


@login_required
def payOfferForm(request, offer_id):
    offer = Offer.objects.get(pk=offer_id)
    solutions_done = offer.issue.getSolutionsDone()
    shared_price = None

    convert_rate = 1
    currency_symbol = "US$"
    alert_brazil = False
    if(offer.sponsor.getUserInfo().brazilianPaypal):
        convert_rate = payment_services.usd_2_brl_convert_rate()
        currency_symbol = "R$"
        alert_brazil = True

    if(solutions_done.count() > 0):
        shared_price = convert_rate * float(offer.price) / solutions_done.count()
        shared_price = twoplaces(Decimal(str(shared_price)))

    return render_to_response('core/pay_offer.html',
        {'offer':offer,
         'solutions_done' : solutions_done,
         'shared_price' : shared_price,
         'convert_rate' : convert_rate,
         'currency_symbol' : currency_symbol,
         'alert_brazil' : alert_brazil,
         },
        context_instance = RequestContext(request))