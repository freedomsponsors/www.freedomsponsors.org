from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from core.models import Payment

__author__ = 'tony'


@user_passes_test(lambda u: u.is_superuser)
def list_payments(request):
    payments = Payment.objects.all().order_by('-creationDate')
    return render_to_response('core2/payment_list.html',
                              {'payments': payments},
                              context_instance=RequestContext(request))


@user_passes_test(lambda u: u.is_superuser)
def view_payment(request, payment_id):
    payment = Payment.objects.get(pk=payment_id)
    return render_to_response('core2/payment.html',
                              {'payment': payment},
                              context_instance=RequestContext(request))

