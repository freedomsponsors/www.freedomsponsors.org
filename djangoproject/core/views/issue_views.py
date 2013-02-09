from django.contrib.auth.decorators import login_required
from django.contrib.syndication.views import Feed
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _
from core.utils.frespo_utils import get_or_none, dictOrEmpty, twoplaces
from core.models import *
from core.services import issue_services, watch_services, payment_services
from decimal import Decimal
import logging
from django.conf import settings
import traceback

logger = logging.getLogger(__name__)

__author__ = 'tony'

@login_required
def addIssue(request):
    try:
        offer = issue_services.sponsor_new_issue(request.POST, request.user)
        watch_services.watch_issue(request.user, offer.issue.id, IssueWatch.SPONSORED)
    except BaseException as ex:
        traceback.print_exc()
        return HttpResponse(_("ERROR: ")+ex.message)
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
        traceback.print_exc()
        return HttpResponse(_("ERROR: ")+ex.message)

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
    accepting_payments = request.POST.has_key('accept_payments')
    issue = issue_services.add_solution_to_existing_issue(issue_id, comment_content, accepting_payments, request.user)
    watch_services.watch_issue(request.user, issue.id, IssueWatch.STARTED_WORKING)
    return redirect(issue.get_view_link())


@login_required
def editOffer(request):
    offer_id = int(request.POST['offer_id'])
    offer = issue_services.change_existing_offer(offer_id, request.POST, request.user)
    return redirect(offer.get_view_link())


def _listIssues(request):
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
    return issues


def listIssues(request):
    project_id = request.GET.get('project_id')
    project_name = request.GET.get('project_name')
    search_terms = request.GET.get('s')
    operation = dictOrEmpty(request.GET, 'operation')
    return render_to_response('core/issue_list.html',
        {'issues':_listIssues(request),
         's':search_terms,
         'project_id':project_id,
         'project_name':project_name,
         'operation':operation,
        },
        context_instance = RequestContext(request))


def listIssuesFeed(request):
    feed_class = LatestIssuesFeed()
    return feed_class(request)


class LatestIssuesFeed(Feed):
    title = "FreedomSponsors.org issues"
    link = "/core/issue/rss"
    description = "Lastest updated FreedomSponsors.org issues."

    def get_object(self, request, *args, **kwargs):
        self._request = request
        return None

    def items(self, obj):
        return _listIssues(self._request)[:20]

    def item_title(self, item):
        return u'(%s) %s' % (item.project, item.title)

    def item_author_name(self, item):
        return item.createdByUser.username

    def item_description(self, item):
        return item.description

    def item_link(self, item):
        return item.get_view_link()

    def item_pubdate(self, item):
        return item.creationDate


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

    issue = Issue.objects.get(pk = issue_id)
    offer = issue_services.sponsor_existing_issue(issue_id, request.POST, request.user)
    watch_services.watch_issue(request.user, issue_id, IssueWatch.SPONSORED)

    invoke_parent_callback = dictOrEmpty(request.POST, 'invoke_parent_callback')
    if(invoke_parent_callback == 'true'):
        params = '?c=s' # c = Callback (iframe javascript callback)
    else:
        params = '?alert=SPONSOR' # a = Alert
    if (issue.getSolutionsAcceptingPayments().count() > 0):
        messages.info(request, 'This issue is open for payments. You are free to choose: you can pay now, or you can wait until after the issue is finished. No pressure :-)')
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
    alert_reputation_revoking = mysolution and mysolution.status == Solution.IN_PROGRESS and mysolution.get_received_payments().count() > 0

    invoke_parent_callback = (dictOrEmpty(request.GET, 'c') == 's')

    is_watching = request.user.is_authenticated() and watch_services.is_watching_issue(request.user, issue.id)

    return render_to_response('core/issue.html',
        {'issue':issue,
        'is_watching':is_watching,
        'myoffer':myoffer,
        'mysolution':mysolution,
        'invoke_parent_callback' : invoke_parent_callback,
        'show_sponsor_popup' : show_sponsor_popup,
        'show_alert' : show_alert,
        'alert_reputation_revoking': alert_reputation_revoking},

        context_instance = RequestContext(request))


def viewOffer(request, offer_id):
    offer = Offer.objects.get(pk=offer_id)
    payment = None
    myoffer = None
    mysolution = None
    show_alert = None

    if(request.user.is_authenticated()):
        mysolution = get_or_none(Solution, issue=offer.issue,programmer=request.user)
        myoffer = get_or_none(Offer, issue=offer.issue,sponsor=request.user)

    alert = dictOrEmpty(request.GET, 'alert')
    if(alert == 'SPONSOR' and offer.issue.project):
        show_alert = 'core/popup_just_sponsored.html'
    alert_reputation_revoking = mysolution and mysolution.status == Solution.IN_PROGRESS and mysolution.get_received_payments().count() > 0
    invoke_parent_callback = (dictOrEmpty(request.GET, 'c') == 's')

    is_watching = request.user.is_authenticated() and watch_services.is_watching_offer(request.user, offer.id)

    return render_to_response('core/offer.html',
        {'offer':offer,
        'is_watching':is_watching,
        'issue':offer.issue,
        'show_alert':show_alert,
        'myoffer':myoffer,
        'mysolution':mysolution,
        'alert_reputation_revoking': alert_reputation_revoking,
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
        'operation' : operation,},
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
    solutions_accepting_payments = offer.issue.getSolutionsAcceptingPayments()
    shared_price = None

    convert_rate = 1
    currency_symbol = "US$"
    alert_brazil = False
    if(offer.sponsor.getUserInfo().brazilianPaypal):
        convert_rate = payment_services.usd_2_brl_convert_rate()
        currency_symbol = "R$"
        alert_brazil = True

    if(solutions_accepting_payments.count() > 0):
        shared_price = convert_rate * float(offer.price) / solutions_accepting_payments.count()
        shared_price = twoplaces(Decimal(str(shared_price)))

    return render_to_response('core/pay_offer.html',
        {'offer':offer,
         'solutions_accepting_payments' : solutions_accepting_payments,
         'shared_price' : shared_price,
         'convert_rate' : convert_rate,
         'currency_symbol' : currency_symbol,
         'alert_brazil' : alert_brazil,
         },
        context_instance = RequestContext(request))
