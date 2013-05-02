from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.translation import ugettext as _
from core.utils import paypal_adapter
from core.utils.frespo_utils import  dictOrEmpty
from core.models import  Payment
from core.services import paypal_services, mail_services
import logging
import traceback

logger = logging.getLogger(__name__)

__author__ = 'tony'

def payOffer(request, offer, payment):
    current_payment_id = dictOrEmpty(request.session, 'current_payment_id')
    if(current_payment_id):
        paypal_services.forget_payment(int(current_payment_id))

    try:
        paypal_adapter.generate_paypal_payment(payment)
    except BaseException as e:
        traceback.print_exc()
        messages.error(request, 'Error communicating with Paypal: %s' % e)
        mail_services.notify_admin('Error generating paypal payment', traceback.format_exc())
        return redirect(offer.get_view_link())
    payment.save()

    request.session['current_payment_id'] = payment.id

    if(settings.PAYPAL_USE_SANDBOX):
        # form_action = 'https://www.sandbox.paypal.com/webapps/adaptivepayment/flow/pay'
        redirect_url = 'https://www.sandbox.paypal.com/webscr?cmd=_ap-payment&paykey=%s' % payment.paykey
    else:
        # form_action = 'https://www.paypal.com/webapps/adaptivepayment/flow/pay'
        redirect_url = 'https://www.paypal.com/webscr?cmd=_ap-payment&paykey=%s' % payment.paykey
    return redirect(redirect_url)


@login_required
def paypalCancel(request):
    if(request.session.has_key('current_payment_id')):
        curr_payment = Payment.objects.get(pk=int(request.session['current_payment_id']))
        if(curr_payment.status != Payment.CONFIRMED_WEB and curr_payment.status != Payment.CONFIRMED_IPN):
            curr_payment.cancel()
            msg = _('Payment canceled')
            logger.info('CANCELED payment %s' % curr_payment.id)
        else:
            msg = _('Error: attempt to cancel a payment already processed')
            curr_payment = None
            logger.warn('attempt to cancel processed payment %s'%curr_payment.id)
        del request.session['current_payment_id']
    else :
        msg = _('Session expired')
        curr_payment = None
        logger.warn('CANCEL received while no payment in session. user = %s'%request.user.id)
    messages.error(request, "Payment canceled.")
    #TODO: Show msg to user
    # return render_to_response('core/paypal_canceled.html',
    #     {'msg':msg,
    #     'payment':curr_payment},
    #     context_instance = RequestContext(request))
    return redirect(curr_payment.offer.issue.get_view_link())

@csrf_exempt
def paypalIPN(request):
    if paypal_adapter.verify_ipn(request.POST.copy()):
        paykey = request.POST['pay_key']
        status = request.POST['status']
        tracking_id = request.POST['tracking_id']
        paypal_services.process_ipn_return(paykey, status, tracking_id)

        return HttpResponse(_("OK"))
    else:
        raise BaseException(_('unverified IPN ')+str(request.POST))


@login_required
@csrf_exempt
def paypalReturn(request):
    current_payment_id = dictOrEmpty(request.session, 'current_payment_id')
    if(current_payment_id):
        curr_payment, msg = paypal_services.payment_confirmed_web(current_payment_id)
        del request.session['current_payment_id']
        logger.info('CONFIRM_WEB successful for payment %s'%curr_payment.id)
    else :
        msg = _('Session expired')
        curr_payment = None
        logger.warn('CONFIRM_WEB received while no payment in session. user = %s'%request.user.id)
    messages.warning(request, "Your payment is being processed. You'll receive an email when your payment is confirmed.")
    # return render_to_response('core/paypal_confirmed.html',
    #     {'msg':msg,
    #     'payment':curr_payment},
    #     context_instance = RequestContext(request))
    return redirect(curr_payment.offer.issue.get_view_link())