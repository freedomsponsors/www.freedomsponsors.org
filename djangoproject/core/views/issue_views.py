import json
from decimal import Decimal
import logging
import traceback

from django.contrib.auth.decorators import login_required
from django.contrib.syndication.views import Feed
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.conf import settings

from core.utils.frespo_utils import get_or_none, twoplaces
from core.models import *
from core.services import issue_services, watch_services, paypal_services, mail_services
from core.views import paypal_views, bitcoin_views, template_folder, HOME_CRUMB
from frespo_currencies import currency_service


logger = logging.getLogger(__name__)

__author__ = 'tony'


@login_required
def addIssue(request):
    try:
        offer = issue_services.sponsor_new_issue(request.POST, request.user)
        watch_services.watch_issue(request.user, offer.issue.id, IssueWatch.SPONSORED)
    except BaseException as ex:
        traceback.print_exc()
        return HttpResponse(_("ERROR: ") + ex.message)
    params = '?alert=SPONSOR'
    to = offer if template_folder(request) == 'core/' else offer.issue
    return  redirect(to.get_view_link() + params)


@login_required
def kickstartIssue(request):
    try:
        issue = issue_services.kickstart_new_issue(request.POST, request.user)
        watch_services.watch_issue(request.user, issue.id, IssueWatch.CREATED)
    except BaseException as ex:
        traceback.print_exc()
        return HttpResponse(_("ERROR: ")+ex.message)

    params = '?alert=KICKSTART'
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
    need_bitcoin_address = _need_to_set_bitcoin_address(request.user, issue)
    need_verify_paypal = _need_to_verify_paypal_account(request.user, issue)
    if need_bitcoin_address:
        msg = """You just began working on an issue with a Bitcoin offer.
You need to configure a Bitcoin address on your user profile, otherwise the sponsor will not be able to pay his offer to you.
You can set your bitcoin address in your 'edit profile' page."""
        messages.error(request, msg)
    if need_verify_paypal:
        msg = """You just began working on an issue with an offer in USD.
FS has detected that the email '%s' is not associated with a verified Paypal account.
You need to have a verified Paypal account before you can receive payments through Paypal.""" % request.user.getUserInfo().paypalEmail
        messages.error(request, msg)
    return redirect(issue.get_view_link())


def _need_to_set_bitcoin_address(user, issue):
    if user.getUserInfo().bitcoin_receive_address:
        return False
    for offer in issue.getOffers():
        if offer.currency == 'BTC':
            return True
    return False


def _need_to_verify_paypal_account(user, issue):
    paypal_verified = paypal_services.accepts_paypal_payments(user)
    if paypal_verified:
        return False
    for offer in issue.getOffers():
        if offer.currency == 'USD':
            return True
    return False


@login_required
def editOffer(request):
    offer_id = int(request.POST['offer_id'])
    offer = issue_services.change_existing_offer(offer_id, request.POST, request.user)
    return redirect(offer.issue.get_view_link())


def _listIssues(request):
    project_id = request.GET.get('project_id')
    project_name = request.GET.get('project_name')
    search_terms = request.GET.get('s')
    operation = request.GET.get('operation', '')
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
    operation = request.GET.get('operation', '')

    issues = _listIssues(request)
    if isinstance(issues, Issue):
        issue = issues
        return redirect(issue.get_view_link())
    if issues.count() == 1:
        issue = issues[0]
        return redirect(issue.get_view_link())

    return render_to_response(template_folder(request) + 'issue_list.html',
        {'issues': issues,
         's': search_terms,
         'project_id': project_id,
         'project_name': project_name,
         'operation': operation,
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
    return render_to_response(template_folder(request) + 'myissues.html',
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

    invoke_parent_callback = request.POST.get('invoke_parent_callback')
    if(invoke_parent_callback == 'true'):
        params = '?c=s' # c = Callback (iframe javascript callback)
    else:
        params = '?alert=SPONSOR' # a = Alert
    if (issue.getSolutionsAcceptingPayments().count() > 0):
        messages.info(request, 'This issue is open for payments. You are free to choose: you can pay now, or you can wait until after the issue is finished. No pressure :-)')
    return redirect(offer.issue.get_view_link() + params)


def _actionbar(issue, myoffer, mysolution, user):
    bar = {}
    bar['sponsor'] = not user.is_authenticated() or not myoffer or myoffer.status != Offer.OPEN
    bar['pay'] = myoffer and myoffer.status == Offer.OPEN
    bar['change'] = bar['pay']
    bar['revoke'] = bar['pay']
    bar['work'] = not user.is_authenticated() or not mysolution or mysolution.status != Solution.IN_PROGRESS
    bar['resolve'] = mysolution and mysolution.status == Solution.IN_PROGRESS
    bar['abort'] = bar['resolve']
    return bar


def viewIssue(request, issue_id):
    issue = Issue.objects.get(pk=issue_id)
    myoffer = None
    mysolution = None
    show_alert = None

    if(request.user.is_authenticated()):
        myoffer = get_or_none(Offer, issue=issue, sponsor=request.user, status__in=[Offer.OPEN, Offer.REVOKED])
        mysolution = get_or_none(Solution, issue=issue,programmer=request.user)

    show_sponsor_popup = (request.GET.get('show_sponsor') == 'true')
    alert = request.GET.get('alert')
    if alert == 'KICKSTART':
        show_alert = template_folder(request) + 'popup/popup_just_kickstarted.html'
    if alert == 'SPONSOR':
        show_alert = template_folder(request) + 'popup/popup_just_sponsored.html'
    alert_reputation_revoking = mysolution and mysolution.status == Solution.IN_PROGRESS and mysolution.get_received_payments().count() > 0

    invoke_parent_callback = (request.GET.get('c') == 's')

    is_watching = request.user.is_authenticated() and watch_services.is_watching_issue(request.user, issue.id)
    crumbs = [HOME_CRUMB, {
        'link': issue.trackerURL,
        'name': 'issue: ' + issue.title,
        'blank': True,
    }]

    context = {
        'issue': issue,
        'is_watching': is_watching,
        'myoffer': myoffer,
        'mysolution': mysolution,
        'invoke_parent_callback': invoke_parent_callback,
        'show_sponsor_popup': show_sponsor_popup,
        'show_alert': show_alert,
        'alert_reputation_revoking': alert_reputation_revoking,
        'crumbs': crumbs,
        'actionbar': _actionbar(issue, myoffer, mysolution, request.user)}

    return render_to_response(template_folder(request) + 'issue.html', context, context_instance=RequestContext(request))


def editIssue(request):
    issue_id = int(request.POST['issue_id'])
    issue = issue_services.change_existing_issue(issue_id, request.POST, request.user)
    return redirect(issue.get_view_link())


def viewOffer(request, offer_id):
    offer = Offer.objects.get(pk=offer_id)
    payment = None
    myoffer = None
    mysolution = None
    show_alert = None

    if(request.user.is_authenticated()):
        mysolution = get_or_none(Solution, issue=offer.issue, programmer=request.user)
        myoffer = get_or_none(Offer, issue=offer.issue, sponsor=request.user, status__in=[Offer.OPEN, Offer.REVOKED])

    alert = request.GET.get('alert')
    if(alert == 'SPONSOR' and offer.issue.project):
        show_alert = 'core/popup/popup_just_sponsored.html'
    alert_reputation_revoking = mysolution and mysolution.status == Solution.IN_PROGRESS and mysolution.get_received_payments().count() > 0
    invoke_parent_callback = (request.GET.get('c') == 's')

    is_watching = request.user.is_authenticated() and watch_services.is_watching_offer(request.user, offer.id)

    return render_to_response(template_folder(request) + 'offer.html',
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
    trackerURL = request.GET.get('trackerURL', '')
    operation = request.GET.get('operation', '')
    if(trackerURL):
        issues = Issue.objects.filter(trackerURL__iexact=trackerURL)
        issue_already_exists = issues.count() >= 1
        if(issues.count() > 1):
            logger.warning("Database inconsistency: more than one issue found with url = %s"%trackerURL)
        if(issue_already_exists):
            return redirect(issues[0].get_view_link()+'?show_sponsor=true&c=s')

    return render_to_response(template_folder(request) + 'add_issue.html',
        {'trackerURL' : trackerURL,
        'operation' : operation,},
        context_instance = RequestContext(request))


def _currency_options(offer):
    is_brazilian = offer.sponsor.getUserInfo().brazilianPaypal
    btc = {'currency': 'BTC',
           'selectLabel': 'Bitcoin',
           'rate': currency_service.get_rate(offer.currency, 'BTC')}
    if is_brazilian:
        brl = {'currency': 'BRL',
               'selectLabel': 'R$, usando Paypal',
               'rate': currency_service.get_rate(offer.currency, 'BRL')}
        return [brl, btc]
    else:
        usd = {'currency': 'USD',
               'selectLabel': 'US$, using Paypal',
               'rate': currency_service.get_rate(offer.currency, 'USD')}
        return [usd, btc]


@login_required
def payOfferForm(request, offer_id):
    offer = Offer.objects.get(pk=offer_id)
    is_brazilian = offer.sponsor.getUserInfo().brazilianPaypal

    solutions_accepting_payments = offer.issue.getSolutionsAcceptingPayments()
    if not solutions_accepting_payments:
        messages.error(request, 'No developers are accepting payments for this issue yet')
        return redirect(offer.issue.get_view_link())

    solutions_dict = []
    for solution in solutions_accepting_payments:
        programmer_userinfo = solution.programmer.getUserInfo()
        try:
            accepts_paypal = paypal_services.accepts_paypal_payments(solution.programmer)
        except BaseException as e:
            traceback.print_exc()
            messages.error(request, 'Error communicating with Paypal: %s' % e)
            mail_services.notify_admin('Error determining if user accepts paypal', traceback.format_exc())
            return redirect(offer.issue.get_view_link())
        solutions_dict.append({
            'id': solution.id,
            'status': solution.status,
            'programmerScreenName': programmer_userinfo.screenName,
            'acceptsPaypal': accepts_paypal,
            'acceptsBitcoin': True and programmer_userinfo.bitcoin_receive_address,
            'imglink': solution.programmer.gravatar_url_small()
        })
    currency_options = _currency_options(offer)
    return render_to_response(template_folder(request) + 'pay_offer_angular.html',
                              {
                                  'offer': offer,
                                  'count': len(solutions_dict),
                                  'currency_options': currency_options,
                                  'currency_options_json': json.dumps(currency_options),
                                  'is_brazilian': is_brazilian,
                                  'solutions_json': json.dumps(solutions_dict)
                              },
                              context_instance=RequestContext(request))

@login_required
def payOffer(request):
    offer_id = int(request.POST['offer_id'])
    offer = Offer.objects.get(pk=offer_id)
    if offer.status == Offer.PAID:
        raise BaseException('offer %s is already paid' % offer.id + '. User %s' % request.user)
    if offer.sponsor.id != request.user.id:
        raise BaseException('offer %s cannot be paid by user %s' % (offer.id, request.user.id))
    payment = _generate_payment_entity(offer, request.POST)
    if payment.currency == 'USD' or payment.currency == 'BRL':
        return paypal_views.payOffer(request, offer, payment)
    elif payment.currency == 'BTC':
        return bitcoin_views.payOffer(request, offer, payment)
    else:
        raise BaseException('Unknown currency: %s' % payment.currency)


def _generate_payment_entity(offer, dict):
    count = int(dict['count'])
    currency = dict['currency']
    payment = Payment.newPayment(offer, currency)
    parts = []
    sum = Decimal(0)
    btc_fee = Decimal(0)
    for i in range(count):
        pay_str = dict['pay_%s' % i]
        solution_id = int(dict['solutionId_%s' % i])
        if(pay_str):
            pay = Decimal(pay_str)
            if pay > 0:
                solution = Solution.objects.get(pk=solution_id)
                solution = Solution.objects.get(pk=solution_id)
                part = PaymentPart.newPart(payment, solution, pay)
                parts.append(part)
                sum += pay
                if currency == 'BTC':
                    btc_fee += settings.BITCOIN_FEE
    payment.fee = sum * settings.FS_FEE
    payment.total = sum
    payment.bitcoin_fee = btc_fee
    convert_twoplaces = currency == 'USD' or currency == 'BRL'
    if convert_twoplaces:
        payment.fee = twoplaces(payment.fee)
        payment.total = twoplaces(payment.total)
    payment.save()
    for part in parts:
        part.payment = payment
        if convert_twoplaces:
            part.price = twoplaces(part.price)
        part.save()
    return payment

