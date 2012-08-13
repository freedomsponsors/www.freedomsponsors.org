# Create your views here.

from django.http import HttpResponseRedirect
from django.contrib.auth import logout as auth_logout
from django.template import Context, loader, RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, redirect
from core.models import *
from django.http import HttpResponse
from exceptions import BaseException
from frespoutils import validateURL, validateIssueURL, get_or_none, getUnconnectedSocialAccounts, dictOrEmpty
from frespomail import *
from django.conf import settings
from frespopaypal import generatePayment, verify_ipn
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)

def _throwIfIssueExists(trackerURL, request):
    if(trackerURL):
        issues = Issue.objects.filter(trackerURL__iexact=trackerURL)
        if(issues.count() >= 1):
            raise BaseException('Already exists: '+trackerURL+". User %s"%request.user.id)

def _throwIfAlreadySponsoring(issue, user):
    offer = get_or_none(Offer, issue=issue, sponsor=user)
    if(offer):
        raise BaseException('Already sponsoring: '+str(issue.id)+','+str(user.id))

def _throwIfNotOfferOwner(offer, user):
    if(not offer.sponsor.id == user.id):
        raise BaseException('Security error. '+str(user.id)+' is not offer ('+str(offer.id)+') owner. (Hey, if you do hack us, have the finesse to let us know, please - we are all firends here, right? ;-)')

def _throwIfNotCommentAuthor(comment, user):
    if(not comment.author.id == user.id):
        raise BaseException('Security error. '+str(user.id)+' is not comment ('+str(comment.id)+') author. (Hey, if you do hack us, have the finesse to let us know, please - we are all firends here, right? ;-)')

def _throwIfNotSolutionOwner(solution, user):
    if(not solution.programmer.id == user.id):
        raise BaseException('Security error. '+str(user.id)+' is not solution ('+str(solution.id)+') owner. (Hey, if you do hack us, have the finesse to let us know, please - we are all firends here, right? ;-)')

def _throwIfOfferNotOpen(offer, user, operation=None):
    if(not offer.status == Offer.OPEN):
        raise BaseException('Error. Expected offer in OPEN state. Found ('+offer.status+'). User '+str(user.id)+'/ offer '+str(offer.id)+'. operation: '+operation)

def _throwIfSolutionNotInProgress(solution, user, operation=None):
    if(not solution.status == Solution.IN_PROGRESS):
        raise BaseException('Error. Expected solution in IN_PROGRESS state. Found ('+solution.status+'). User '+str(user.id)+'/ solution '+str(solution.id)+'. operation: '+operation)

def _throwIfSolutionInProgress(solution, user, operation=None):
    if(solution.status == Solution.IN_PROGRESS):
        raise BaseException('Error: found solution in progress '+str(solution.id)+', '+str(user.id)+'. operation: '+operation)

def _setOfferAttributesFromRequest(offer, request):
    offer.price = Decimal(request.POST['price'])
    offer.no_forking = request.POST.has_key('no_forking')
    offer.require_release = request.POST.has_key('require_release')
    offer_check_expires = request.POST.has_key('expires')
    if(offer_check_expires):
        offer.set_expiration_days(int(request.POST['expiration_time']))
    offer.acceptanceCriteria = request.POST['acceptanceCriteria']

    if(not offer.acceptanceCriteria):
        raise BaseException('acceptanceCriteria is required')

    if(offer.price <= 0):
        raise BaseException('offer price must be a positive number')

def _buildOfferFromRequest_and_issue(request, issue):
    offer = Offer.newOffer(issue, request.user, Decimal(0), '', False, False, None)
    _setOfferAttributesFromRequest(offer, request)
    return offer
    

def _buildOfferFromRequest(request):
    check_noProject = request.POST.has_key('noProject')
    issue_trackerURL = request.POST['trackerURL']
    issue_projectId = request.POST['project_id']
    issue_projectName = dictOrEmpty(request.POST, 'project_name')
    check_createProject = request.POST.has_key('createProject')
    newProject_name = dictOrEmpty(request.POST, 'newProjectName')
    newProject_homeURL = dictOrEmpty(request.POST, 'newProjectHomeURL')
    newProject_trackerURL = dictOrEmpty(request.POST, 'newProjectTrackerURL')
    issue_key = dictOrEmpty(request.POST, 'key');
    issue_title = dictOrEmpty(request.POST, 'title');
    issue_description = dictOrEmpty(request.POST, 'description');

    _throwIfIssueExists(issue_trackerURL, request)

    issue = None
    if(check_noProject):
        if(not issue_title or not issue_description):
            raise BaseException('title and description are required')

        issue = Issue.newIssueOrphan(issue_title, issue_description, request.user)
    else:
        project = None
        if(check_createProject):
            if(not newProject_name or not newProject_homeURL or not newProject_trackerURL):
                raise BaseException('all parameters for new project are required')

            projectHomeURLValidationError = validateURL(newProject_homeURL)
            if(projectHomeURLValidationError):
                raise BaseException('invalid project URL ('+newProject_homeURL+') - '+projectHomeURLValidationError)

            projectTrackerURLValidationError = validateURL(newProject_trackerURL)
            if(projectTrackerURLValidationError):
                raise BaseException('invalid project tracker URL ('+newProject_trackerURL+') - '+projectTrackerURLValidationError)

            project = Project.newProject(newProject_name, request.user, newProject_homeURL, newProject_trackerURL)
        else:
            project = Project.objects.get(pk=int(issue_projectId))
            if(newProject_homeURL != project.homeURL):
                project.homeURL = newProject_homeURL

        if(not issue_key or not issue_title):
            raise BaseException('key and title are required')

        issueURLValidationError = validateIssueURL(issue_trackerURL)
        if(issueURLValidationError):
            raise BaseException('invalid issue URL ('+issue_trackerURL+') - '+issueURLValidationError)

        issue = Issue.newIssue(project, issue_key, issue_title, request.user, issue_trackerURL)

    return _buildOfferFromRequest_and_issue(request, issue);



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


def home(request):
    if(request.user.is_authenticated() and request.user.getUserInfo() == None):
        return redirect('/core/user/edit')
    issues = Issue.listIssues()[0:10]
    return render_to_response('core/home.html',
        {'issues':issues},
        context_instance = RequestContext(request))

def myissues(request):
    if(request.user.is_authenticated() and request.user.getUserInfo() == None):
        return redirect('/core/user/edit')
    return render_to_response('core/myissues.html',
        {},
        context_instance = RequestContext(request))


def listIssues(request):
    issues = Issue.objects.all()
    project_id = request.GET.get('project_id')
    project_name = request.GET.get('project_name')
    s = request.GET.get('s')
    if project_id :
        issues = issues.filter(project__id=project_id)
    elif project_name :
        issues = issues.filter(project__name__icontains=project_name)
    if s :
        issues = issues.filter(title__icontains=s)
    issues = issues.order_by('-creationDate')
    return render_to_response('core/issue_list.html',
        {'issues':issues,
         's':s,
         'project_id':project_id,
         'project_name':project_name,
        },
        context_instance = RequestContext(request))

def listProjects(request):
    projects = Project.objects.all()
    projects = projects.order_by('name')
    return render_to_response('core/project_list.html',
        {'projects':projects},
        context_instance = RequestContext(request))

def viewOffer(request, offer_id):
    offer = Offer.objects.get(pk=offer_id)
    myoffer = None
    mysolution = None
    show_alert = None

    if(request.user.is_authenticated()):
        mysolution = get_or_none(Solution, issue=offer.issue,programmer=request.user)
        myoffer = get_or_none(Offer, issue=offer.issue,sponsor=request.user)

    a = dictOrEmpty(request.GET, 'a')
    if(a == 's' and offer.issue.project):
        show_alert = 'core/popup_just_sponsored.html'
    invoke_parent_callback = (dictOrEmpty(request.GET, 'c') == 's')

    return render_to_response('core/offer.html',
        {'offer':offer,
        'issue':offer.issue,
        'show_alert':show_alert,
        'myoffer':myoffer,
        'mysolution':mysolution,
        'invoke_parent_callback' : invoke_parent_callback},
        context_instance = RequestContext(request))

@login_required
def payOfferForm(request, offer_id):
    offer = Offer.objects.get(pk=offer_id)
    solutions_done = offer.issue.getSolutionsDone()
    shared_price = None
    
    convert_rate = 1
    currency_symbol = "U$"
    alert_brazil = False
    if(offer.sponsor.getUserInfo().brazilianPaypal):
        convert_rate = 2
        currency_symbol = "R$"
        alert_brazil = True
        
    if(solutions_done.count() > 0):
        shared_price = convert_rate* offer.price / solutions_done.count()

    return render_to_response('core/pay_offer.html',
        {'offer':offer,
         'solutions_done' : solutions_done,
         'shared_price' : shared_price,
         'convert_rate' : convert_rate,
         'currency_symbol' : currency_symbol,
         'alert_brazil' : alert_brazil,
         },
        context_instance = RequestContext(request))

def viewIssue(request, issue_id):
    issue = Issue.objects.get(pk=issue_id)
    myoffer = None
    mysolution = None

    if(request.user.is_authenticated()):
        myoffer = get_or_none(Offer, issue=issue,sponsor=request.user)
        mysolution = get_or_none(Solution, issue=issue,programmer=request.user)

    show_sponsor_popup = (dictOrEmpty(request.GET, 'show_sponsor') == 'true')
    invoke_parent_callback = (dictOrEmpty(request.GET, 'c') == 's')

    return render_to_response('core/issue.html',
        {'issue':issue,
        'myoffer':myoffer,
        'mysolution':mysolution,
        'invoke_parent_callback' : invoke_parent_callback,
        'show_sponsor_popup' : show_sponsor_popup},
        
        context_instance = RequestContext(request))

@login_required
def addIssueForm(request):
    trackerURL = dictOrEmpty(request.GET, 'trackerURL')
    if(request.user.getUserInfo() == None):
        redirectPath = '/core/user/edit'
        if(trackerURL):
            redirectPath += '?next=/core/issue/add%3FtrackerURL%3D'+trackerURL
        return redirect(redirectPath)
    if(trackerURL):
        issues = Issue.objects.filter(trackerURL__iexact=trackerURL)
        issue_already_exists = issues.count() >= 1
        if(issues.count() > 1):
            logger.warning("Database inconsistency: more than one issue found with url = %s"%trackerURL)
        if(issue_already_exists):
            return redirect(issues[0].get_view_link()+'?show_sponsor=true&c=s')

    return render_to_response('core/add_issue.html',
        {'trackerURL' : trackerURL},
        context_instance = RequestContext(request))
    

@login_required
def addIssue(request):
    try:
        offer = _buildOfferFromRequest(request)
    except BaseException as ex:
        return HttpResponse("ERROR: "+ex.message)
    if(offer.issue.project):
        offer.issue.project.save()
        offer.issue.project = offer.issue.project
    if(not offer.issue.id):
        offer.issue.save()
        offer.issue = offer.issue
    offer.save()
    msg = "offer: "+str(offer.price)+"\n<br>"+ \
        "issue key: "+offer.issue.key+"\n<br>"+ \
        "issue title: "+offer.issue.title+"\n<br>"
    if(offer.issue.project):
        msg += "project : "+offer.issue.project.name+"\n<br>"+ \
        "project.trackerURL: "+offer.issue.project.trackerURL+"\n<br>"
    notify_admin("INFO: New issue sponsored", msg)
    
    if(dictOrEmpty(request.POST, 'invoke_parent_callback') == 'true'):
        params = '?c=s' # c = Callback (iframe javascript callback)
    else:
        params = '?a=s' # a = Alert
    return redirect(offer.get_view_link()+params)

@login_required
def sponsorIssue(request):
    issue = Issue.objects.get(pk=int(request.POST['issue_id']))
    invoke_parent_callback = dictOrEmpty(request.POST, 'invoke_parent_callback')

    _throwIfAlreadySponsoring(issue, request.user)

    offer = _buildOfferFromRequest_and_issue(request, issue);
    offer.save()

    notifyProgrammers_offeradded(offer)
    notifySponsors_offeradded(offer)
    msg = "offer: "+str(offer.price)+"\n<br>"+ \
        "issue key: "+offer.issue.key+"\n<br>"+ \
        "issue title: "+offer.issue.title+"\n<br>"
    if(offer.issue.project):
        msg += "project : "+offer.issue.project.name+"\n<br>"+ \
        "project.trackerURL: "+offer.issue.project.trackerURL+"\n<br>"
    notify_admin("INFO: Existing issue sponsored", msg)

    if(dictOrEmpty(request.POST, 'invoke_parent_callback') == 'true'):
        params = '?c=s' # c = Callback (iframe javascript callback)
    else:
        params = '?a=s' # a = Alert
    return redirect(offer.get_view_link()+params)

@login_required
def editOffer(request):
    offer = Offer.objects.get(pk=int(request.POST['offer_id']))
    offer_price = request.POST['price']
    offer_acceptanceCriteria = request.POST['acceptanceCriteria']

    _throwIfNotOfferOwner(offer, request.user)

    old_offer = offer.clone()

    offer.changeOffer(request.POST)

    notifyProgrammers_offerchanged(old_offer, offer)

    return redirect(offer.get_view_link())

@login_required
def addIssueComment(request):
    issue = Issue.objects.get(pk=int(request.POST['issue_id']))
    content = request.POST['content']
    comment = IssueComment.newComment(issue, request.user, content)
    comment.save()
    notifyProgrammers_newissuecomment(comment)
    notifySponsors_newissuecomment(comment)
    return redirect(issue.get_view_link())

@login_required
def editIssueComment(request):
    comment = IssueComment.objects.get(pk=int(request.POST['comment_id']))
    _throwIfNotCommentAuthor(comment, request.user)
    content = request.POST['content']
    comment.changeContent(content)
    return redirect(comment.issue.get_view_link())

@login_required
def addOfferComment(request):
    offer = Offer.objects.get(pk=int(request.POST['offer_id']))
    content = request.POST['content']
    comment = OfferComment.newComment(offer, request.user, content)
    comment.save()
    notifyProgrammers_newoffercomment(comment)
    notifySponsors_newoffercomment(comment)
    return redirect(offer.get_view_link())

@login_required
def editOfferComment(request):
    comment = OfferComment.objects.get(pk=int(request.POST['comment_id']))
    _throwIfNotCommentAuthor(comment, request.user)
    content = request.POST['content']
    comment.changeContent(content)
    return redirect(comment.offer.get_view_link())

@login_required
def revokeOffer(request):
    offer = Offer.objects.get(pk=int(request.POST['offer_id']))
    content = request.POST['comment']

    _throwIfNotOfferOwner(offer, request.user)
    _throwIfOfferNotOpen(offer, request.user, 'revoke offer')

    offer.revoke()

    comment = None
    if(content):
        comment = OfferComment.newComment(offer, request.user, content)
        comment.save()

    notifyProgrammers_offerrevoked(offer, comment)

    return redirect(offer.issue.get_view_link())

@login_required
def payOffer(request):
    offer = Offer.objects.get(pk=int(request.POST['offer_id']))
    if(offer.status == Offer.PAID):
        raise BaseException('offer %s is already paid'%offer.id+'. User %s'%request.user)
    count = int(request.POST['count'])
    if(request.session.has_key('current_payment_id')):
        curr_payment = Payment.objects.get(pk=int(request.session['current_payment_id']))
        if(curr_payment.status != Payment.CONFIRMED_WEB and curr_payment.status != Payment.CONFIRMED_IPN):
            curr_payment.forget()

    payment = Payment.newPayment(offer)
    parts = []
    sum = Decimal(0)
    realSum = Decimal(0)
    for i in range(count):
        check = request.POST.has_key('check_%s'%i)
        if(check):
            solution = Solution.objects.get(pk=int(request.POST['solutionId_%s'%i]))
            pay = Decimal(request.POST['pay_%s'%i])
            realPay = Decimal(pay*Decimal(1-settings.FS_FEE))
            part = PaymentPart.newPart(payment, solution.programmer, pay, realPay)
            parts.append(part)
            sum += pay
            realSum += realPay

    payment.fee = sum - realSum
    payment.total = sum
    payment.save()
    for part in parts:
        part.payment = payment
        part.save()

    generatePayment(payment)
    payment.save()

    request.session['current_payment_id'] = payment.id

    if(settings.PAYPAL_USE_SANDBOX):
        form_action = 'https://www.sandbox.paypal.com/webapps/adaptivepayment/flow/pay'
    else:
        form_action = 'https://www.paypal.com/webapps/adaptivepayment/flow/pay'

    return render_to_response('core/waitPayment.html',
        {'offer' : offer,
        'paykey':payment.paykey,
        'form_action':form_action},
        context_instance = RequestContext(request))

@login_required
def paypalCancel(request):
    if(request.session.has_key('current_payment_id')):
        curr_payment = Payment.objects.get(pk=int(request.session['current_payment_id']))
        if(curr_payment.status != Payment.CONFIRMED_WEB and curr_payment.status != Payment.CONFIRMED_IPN):
            curr_payment.cancel()
            msg = 'Payment canceled'
            logger.info('CANCELED payment %s'%curr_payment.id)
        else:
            msg = 'Error: attempt to cancel a payment already processed'
            curr_payment = None
            logger.warn('attempt to cancel processed payment %s'%curr_payment.id)
        del request.session['current_payment_id']
    else :
        msg = 'Session expired'
        curr_payment = None
        logger.warn('CANCEL received while no payment in session. user = %s'%request.user.id)
    return render_to_response('core/paypal_canceled.html',
        {'msg':msg,
        'payment':curr_payment},
        context_instance = RequestContext(request))

@login_required
@csrf_exempt
def paypalReturn(request):
    if(request.session.has_key('current_payment_id')):
        curr_payment = Payment.objects.get(pk=int(request.session['current_payment_id']))
        curr_payment.confirm_web()
        curr_payment.offer.paid()
        msg = 'Payment confirmed'
        notifyProgrammers_paymentconfirmed(curr_payment) #TODO Mover pro IPN
        del request.session['current_payment_id']
        logger.info('CONFIRM_WEB successful for payment %s'%curr_payment.id)
    else : 
        msg = 'Session expired'
        curr_payment = None
        logger.warn('CONFIRM_WEB received while no payment in session. user = %s'%request.user.id)
    return render_to_response('core/paypal_confirmed.html',
        {'msg':msg,
        'payment':curr_payment},
        context_instance = RequestContext(request))

@csrf_exempt
def paypalIPN(request):
    if verify_ipn(request.POST.copy()):
        paykey = request.POST['pay_key']
        status = request.POST['status']
        if(status == 'COMPLETED'):
            payment = get_or_none(Payment, paykey=paykey)
            if(not payment):
                raise BaseException('payment not found '+paykey)
            payment.confirm_ipn()
            payment.offer.paid()
        else:
            logger.warn('received a '+status+' IPN confirmation')

        return HttpResponse("OK")
    else:
        raise BaseException('unverified IPN '+str(request.POST))

@login_required
def addSolution(request):
    """Start working on this issue"""
    issue = Issue.objects.get(pk=int(request.POST['issue_id']))
    content = request.POST['comment']

    solution = get_or_none(Solution, issue = issue, programmer = request.user)
    if(solution):
        _throwIfSolutionInProgress(solution, request.user, 'add solution')
        solution.reopen()
    else:
        solution = Solution.newSolution(issue, request.user)
    solution.save()

    comment = None
    if(content):
        comment = IssueComment.newComment(issue, request.user, content)
        comment.save()

    notifySponsors_workbegun(solution, comment)

    return redirect(issue.get_view_link())

@login_required
def abortSolution(request):
    solution = Solution.objects.get(pk=int(request.POST['solution_id']))
    content = request.POST['comment']

    _throwIfNotSolutionOwner(solution, request.user)
    _throwIfSolutionNotInProgress(solution, request.user, 'abort solution')

    solution.abort()

    comment = None
    if(content):
        comment = IssueComment.newComment(solution.issue, request.user, content)
        comment.save()

    notifySponsors_workstopped(solution, comment)

    return redirect(solution.issue.get_view_link())

@login_required
def resolveSolution(request):
    solution = Solution.objects.get(pk=int(request.POST['solution_id']))
    content = request.POST['comment']

    _throwIfNotSolutionOwner(solution, request.user)
    _throwIfSolutionNotInProgress(solution, request.user, 'resolve solution')

    solution.resolve()

    comment = None
    if(content):
        comment = IssueComment.newComment(solution.issue, request.user, content)
        comment.save()

    notifySponsors_workdone(solution, comment)
    notifyProgrammers_workdone(solution, comment)

    return redirect(solution.issue.get_view_link())

