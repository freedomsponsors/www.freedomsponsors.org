from datetime import datetime
from core.models import *
from django.db.models import Q
from django.utils.datetime_safe import date
from aggregate_if import Sum, Count


LAUNCH_DATE = datetime(2012, 7, 8)

def get_offer_stats():
    return Offer.objects.aggregate(
        sponsor_count=Count('sponsor', distinct=True),
        offer_count=Count('pk'),
        paid_offer_count=Count('pk', only=Q(status=Offer.PAID)),
        open_offer_count=Count('pk', only=Q(status=Offer.OPEN)), # FIXME: Should OPEN ignore EXPIRED?
        revoked_offer_count=Count('pk', only=Q(status=Offer.REVOKED)),
        paid_sum=Sum('price', only=Q(status=Offer.PAID)),
        open_sum=Sum('price', only=Q(status=Offer.OPEN) & (Q(expirationDate=None) | Q(expirationDate__gt=date.today()))),
        expired_sum=Sum('price', only=Q(status=Offer.OPEN) & Q(expirationDate__lte=date.today())),
        revoked_sum=Sum('price', only=Q(status=Offer.REVOKED)),
    )

def get_issue_stats():
    return Issue.objects.filter(is_feedback=False).aggregate(
        issue_count=Count('pk'),
        issue_project_count=Count('project', distinct=True),
        issue_count_kickstarting=Count('pk', only=Q(is_public_suggestion=True)),
        issue_count_sponsoring=Count('pk', only=Q(is_public_suggestion=False)),
    )

def get_stats():
    stats = {
        'age' : _age(),
        'user_count' : UserInfo.objects.count(),
        'programmer_count' : Solution.objects.aggregate(Count('programmer', distinct=True))['programmer__count'] or 0,
        'paid_programmer_count' : PaymentPart.objects.filter(payment__status='CONFIRMED_IPN').aggregate(Count('programmer', distinct=True))['programmer__count'] or 0,
        'sponsors' : UserInfo.objects.annotate(
                         paid_amount=Sum('user__offer__price', only=Q(user__offer__status=Offer.PAID)),
                         open_amount=Sum('user__offer__price', only=Q(user__offer__status=Offer.OPEN)),
                     ).order_by('-paid_amount'),
        'projects' : Project.objects.annotate(issue_count=Count('issue', distinct=True), offer_sum=Sum('issue__offer__price')).order_by('-offer_sum'),
    }

    stats.update(get_offer_stats())
    stats.update(get_issue_stats())

    return stats

def _age():
    delta = (datetime.today() - LAUNCH_DATE).days
    months = int(delta/30.5)
    weeks = (delta - int(months * 30.5))/7
    s = "%s months" % months
    if weeks > 0:
        s += " and %s week" % weeks
        if(weeks > 1):
            s += "s"
    return s;
