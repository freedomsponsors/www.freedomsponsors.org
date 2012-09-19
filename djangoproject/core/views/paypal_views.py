from decimal import Decimal
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from core.frespomail import notifyProgrammers_paymentconfirmed
from core.frespopaypal import generatePayment, verify_ipn
from core.frespoutils import get_or_none
from core.models import Offer, Payment, Solution, PaymentPart
import logging

logger = logging.getLogger(__name__)

__author__ = 'tony'

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
def payOfferForm(request, offer_id):
    offer = Offer.objects.get(pk=offer_id)
    solutions_done = offer.issue.getSolutionsDone()
    shared_price = None

    convert_rate = 1
    currency_symbol = "US$"
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