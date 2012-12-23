from datetime import datetime, timedelta
import math
from core.models import *
from django.db import connection, transaction
from django.db.models import Q
from django.db.models import Count
from django.utils.datetime_safe import date
from aggregate_if import Sum


SELECT_SPONSORED_PROJECTS = """select pr.id, pr.name, count(i.id) c, sum(o.price) s
from core_project pr, core_issue i, core_offer o
where pr.id = i.project_id and i.id = o.issue_id
group by pr.id, pr.name
order by s desc"""

COUNT_SPONSORS = "select count(distinct sponsor_id) from core_offer"
COUNT_PROGRAMMERS = "select count(distinct programmer_id) from core_solution"
COUNT_PAID_PROGRAMMERS = """select count(distinct pr.programmer_id) 
from core_paymentpart pr, core_payment pa
where pr.payment_id = pa.id
and pa.status = 'CONFIRMED_IPN'"""

COUNT_OFFERS = "select count(*) from core_offer"
COUNT_OFFERS_PAID = "select count(*) from core_offer where status = 'PAID'"
COUNT_OFFERS_OPEN = "select count(*) from core_offer where status = 'OPEN'"
COUNT_OFFERS_REVOKED = "select count(*) from core_offer where status = 'REVOKED'"

SUM_PAID = "select sum (price) from core_offer where status = 'PAID'"



SUM_REVOKED = "select sum (price) from core_offer where status = 'REVOKED'"

LAUNCH_DATE = datetime(2012, 7, 8)

def get_stats():
    return {
        'age' : _age(),
        'user_count' : UserInfo.objects.count(),
        'sponsor_count' : _count(COUNT_SPONSORS),
        'programmer_count' : _count(COUNT_PROGRAMMERS),
        'paid_programmer_count' : _count(COUNT_PAID_PROGRAMMERS),
        'offer_count' : _count(COUNT_OFFERS),
        'issue_count' : Issue.objects.filter(is_feedback=False).count(),
        'issue_project_count' : Issue.objects.filter(is_feedback=False).aggregate(Count('project', distinct=True))['project__count'],
        'issue_count_kickstarting' : Issue.objects.filter(is_feedback=False, is_public_suggestion=True).count(),
        'issue_count_sponsoring' : Issue.objects.filter(is_feedback=False, is_public_suggestion=False).count(),
        'paid_offer_count' : _count(COUNT_OFFERS_PAID),
        'open_offer_count' : _count(COUNT_OFFERS_OPEN),
        'revoked_offer_count' : _count(COUNT_OFFERS_REVOKED),
        'paid_sum' : _sum(SUM_PAID),
        'open_sum' : Offer.objects.filter(status='OPEN').filter(Q(expirationDate=None) | Q(expirationDate__gt=date.today())).aggregate(Sum('price'))['price__sum'] or 0,
        'expired_sum' : Offer.objects.filter(status='OPEN').filter(Q(expirationDate__lte=date.today())).aggregate(Sum('price'))['price__sum'] or 0,
        'revoked_sum' : _sum(SUM_REVOKED),
        'sponsors' : UserInfo.objects.annotate(
                         paid_ammount=Sum('user__offer__price', only=Q(user__offer__status='PAID')),
                         open_ammount=Sum('user__offer__price', only=Q(user__offer__status='OPEN')),
                     ).order_by('-paid_ammount'),
        'projects' : _select(SELECT_SPONSORED_PROJECTS),
    }

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

def _count(query):
    return int(_sum(query))

def _sum(query):
    rows = _select(query)
    r = rows[0][0]
    if r is None:
        r = 0
    return r

def _select(query):
    cursor = connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    return rows
