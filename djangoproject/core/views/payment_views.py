from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django.template.context import RequestContext
from core.models import Payment

__author__ = 'tony'


@user_passes_test(lambda u: u.is_superuser)
def list_payments(request):
    payments = Payment.objects.all().order_by('-creationDate')
    return render(request, 'core2/payment_list.html',
                              {'payments': payments})


@user_passes_test(lambda u: u.is_superuser)
def view_payment(request, payment_id):
    payment = Payment.objects.get(pk=payment_id)
    return render(request, 'core2/payment.html',
                              {'payment': payment})

