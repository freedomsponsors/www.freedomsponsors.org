from datetime import datetime, timedelta
import math
from core.models import *
from django.db import connection, transaction

SELECT_SPONSORS = """select ui.user_id, ui."screenName", sum(o.price) s
from auth_user u, core_offer o, core_userinfo ui
where o.sponsor_id = u.id
and ui.user_id = u.id
and o.status = 'OPEN'
and (o."expirationDate" > now() or o."expirationDate" is null)
group by ui.user_id, ui."screenName"
order by s desc"""

COUNT_SPONSORS = "select count(distinct sponsor_id) from core_offer"

COUNT_PROGRAMMERS = "select count(distinct programmer_id) from core_solution"

COUNT_OFFERS = "select count(*) from core_offer"
COUNT_ISSUES = "select count(*) from core_issue where is_feedback = false"
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
        'offer_count' : _count(COUNT_OFFERS),
        'issue_count' : _count(COUNT_ISSUES),
        'paid_offer_count' : _count(COUNT_OFFERS_PAID),
        'open_offer_count' : _count(COUNT_OFFERS_OPEN),
        'revoked_offer_count' : _count(COUNT_OFFERS_REVOKED),
        'paid_sum' : _sum(SUM_PAID),
        'open_sum' : _sum(SUM_OPEN),
        'expired_sum' : _sum(SUM_EXPIRED),
        'revoked_sum' : _sum(SUM_REVOKED),
        'sponsors' : _select(SELECT_SPONSORS),
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
