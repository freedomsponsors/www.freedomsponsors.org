from datetime import datetime, timedelta
import math
from core.models import *
from django.db import connection, transaction
from django.db.models import Count

SELECT_SPONSORS = """select t.user_id, t."screenName", sum(p1), sum(p2), coalesce(sum(p1), 0) + coalesce(sum(p2), 0) as s3
from (select o.id, ui.user_id, ui."screenName", o.price as p1, null as p2
    from core_userinfo ui, core_offer o
    where o.sponsor_id = user_id 
    and o.status = 'OPEN' 
    and (o."expirationDate" > now() or o."expirationDate" is null)
    union
    select o.id, ui.user_id, ui."screenName", null as p1, o.price as p2
    from core_userinfo ui, core_offer o
    where o.sponsor_id = user_id 
    and o.status = 'PAID') t
group by t.user_id, t."screenName"
order by s3 desc"""

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
COUNT_ISSUES_SPONSORING = "select count(*) from core_issue where is_feedback = false and is_public_suggestion = false"
COUNT_ISSUES_KICKSTARTING = "select count(*) from core_issue where is_feedback = false and is_public_suggestion = true"
COUNT_OFFERS_PAID = "select count(*) from core_offer where status = 'PAID'"
COUNT_OFFERS_OPEN = "select count(*) from core_offer where status = 'OPEN'"
COUNT_OFFERS_REVOKED = "select count(*) from core_offer where status = 'REVOKED'"

SUM_PAID = "select sum (price) from core_offer where status = 'PAID'"

SUM_OPEN = """select sum (price) from core_offer where status = 'OPEN' and ("expirationDate" is null or "expirationDate" > now())"""

SUM_EXPIRED = """select sum (price) from core_offer where status = 'OPEN' and "expirationDate" <= now()"""

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
        'issue_count_kickstarting' : _count(COUNT_ISSUES_KICKSTARTING),
        'issue_count_sponsoring' : _count(COUNT_ISSUES_SPONSORING),
        'issue_count' : Issue.objects.filter(is_feedback=False).count(),
        'issue_project_count' : Issue.objects.filter(is_feedback=False).aggregate(Count('project', distinct=True))['project__count'],
        'paid_offer_count' : _count(COUNT_OFFERS_PAID),
        'open_offer_count' : _count(COUNT_OFFERS_OPEN),
        'revoked_offer_count' : _count(COUNT_OFFERS_REVOKED),
        'paid_sum' : _sum(SUM_PAID),
        'open_sum' : _sum(SUM_OPEN),
        'expired_sum' : _sum(SUM_EXPIRED),
        'revoked_sum' : _sum(SUM_REVOKED),
        'sponsors' : _select(SELECT_SPONSORS),
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
