from datetime import datetime, timedelta
import math
from core.models import *
from django.db import connection, transaction

SELECT_SPONSORS = """
select 
  ui.user_id, 
  ui."screenName",
  count(o.id) cOffer,
  sum(case when (o.status = 'PAID' and o.currency = 'USD') then o.price else 0 end) spaidUSD,
  sum(case when (o.status = 'OPEN' and (o."expirationDate" is null or o."expirationDate" > now()) and o.currency = 'USD') then o.price else 0 end) sopenUSD,
  sum(case when (o.status = 'PAID' and o.currency = 'BTC') then o.price else 0 end) spaidBTC,
  sum(case when (o.status = 'OPEN' and (o."expirationDate" is null or o."expirationDate" > now()) and o.currency = 'BTC') then o.price else 0 end) sopenBTC
from core_userinfo ui, core_offer o
where
  o.sponsor_id = ui.user_id
group by ui.user_id, ui."screenName"
having sum(case when (o.status = 'PAID' and o.currency = 'USD') then o.price else 0 end) > 0
    or sum(case when (o.status = 'OPEN' and (o."expirationDate" is null or o."expirationDate" > now()) and o.currency = 'USD') then o.price else 0 end) > 0
    or sum(case when (o.status = 'PAID' and o.currency = 'BTC') then o.price else 0 end) > 0
    or sum(case when (o.status = 'OPEN' and (o."expirationDate" is null or o."expirationDate" > now()) and o.currency = 'BTC') then o.price else 0 end) > 0
order by sum(case when (o.status = 'PAID' and o.currency = 'USD') then o.price else 0 end) +
     sum(case when (o.status = 'OPEN' and (o."expirationDate" is null or o."expirationDate" > now()) and o.currency = 'USD') then o.price else 0 end)
     desc
"""

SELECT_SPONSORED_PROJECTS = """
select 
  pr.id, 
  pr.name, 
  count(distinct i.id) cIssues, 
  count(o.id) cOffers, 
  sum(case when (o.status = 'PAID' and o.currency = 'USD') then o.price else 0 end) spaidUSD,
  sum(case when (o.status = 'OPEN' and (o."expirationDate" is null or o."expirationDate" > now()) and o.currency = 'USD') then o.price else 0 end) sopenUSD,
  sum(case when (o.status = 'PAID' and o.currency = 'BTC') then o.price else 0 end) spaidBTC,
  sum(case when (o.status = 'OPEN' and (o."expirationDate" is null or o."expirationDate" > now()) and o.currency = 'BTC') then o.price else 0 end) sopenBTC
from core_project pr, core_issue i, core_offer o
where pr.id = i.project_id 
and i.id = o.issue_id
group by pr.id, pr.name
having sum(case when (o.status = 'PAID' and o.currency = 'USD') then o.price else 0 end) > 0
    or sum(case when (o.status = 'OPEN' and (o."expirationDate" is null or o."expirationDate" > now()) and o.currency = 'USD') then o.price else 0 end) > 0
    or sum(case when (o.status = 'PAID' and o.currency = 'BTC') then o.price else 0 end) > 0
    or sum(case when (o.status = 'OPEN' and (o."expirationDate" is null or o."expirationDate" > now()) and o.currency = 'BTC') then o.price else 0 end) > 0
order by sum(case when (o.status = 'PAID' and o.currency = 'USD') then o.price else 0 end) + 
     sum(case when (o.status = 'OPEN' and (o."expirationDate" is null or o."expirationDate" > now()) and o.currency = 'USD') then o.price else 0 end)
     desc
"""

COUNT_SPONSORS = "select count(distinct sponsor_id) from core_offer"
COUNT_PROGRAMMERS = "select count(distinct programmer_id) from core_solution"
COUNT_PAID_PROGRAMMERS = """select count(distinct pr.programmer_id) 
from core_paymentpart pr, core_payment pa
where pr.payment_id = pa.id
and pa.status = 'CONFIRMED_IPN'"""

COUNT_OFFERS = "select count(*) from core_offer"
COUNT_ISSUES = "select count(*) from core_issue where is_feedback = false"
COUNT_ISSUES_SPONSORING = "select count(*) from core_issue where is_feedback = false and is_public_suggestion = false"
COUNT_ISSUES_KICKSTARTING = "select count(*) from core_issue where is_feedback = false and is_public_suggestion = true"
COUNT_OFFERS_PAID = "select count(*) from core_offer where status = 'PAID'"
COUNT_OFFERS_OPEN = "select count(*) from core_offer where status = 'OPEN'"
COUNT_OFFERS_REVOKED = "select count(*) from core_offer where status = 'REVOKED'"
COUNT_PROJECTS = "select count(distinct project_id) from core_issue where is_feedback = false"

SUM_PAID_USD = "select sum (price) from core_offer where status = 'PAID' and currency = 'USD'"
SUM_PAID_BTC = "select sum (price) from core_offer where status = 'PAID' and currency = 'BTC'"

SUM_OPEN_USD = """select sum (price) from core_offer where status = 'OPEN' and currency = 'USD' and ("expirationDate" is null or "expirationDate" > now())"""
SUM_OPEN_BTC = """select sum (price) from core_offer where status = 'OPEN' and currency = 'BTC' and ("expirationDate" is null or "expirationDate" > now())"""

SUM_EXPIRED_USD = """select sum (price) from core_offer where status = 'OPEN' and currency = 'USD' and "expirationDate" <= now()"""
SUM_EXPIRED_BTC = """select sum (price) from core_offer where status = 'OPEN' and currency = 'BTC' and "expirationDate" <= now()"""

SUM_REVOKED_USD = "select sum (price) from core_offer where status = 'REVOKED' and currency = 'USD'"
SUM_REVOKED_BTC = "select sum (price) from core_offer where status = 'REVOKED' and currency = 'BTC'"

LAUNCH_DATE = datetime(2012, 7, 8)

def get_stats():
    return {
        'age' : _age(),
        'user_count' : UserInfo.objects.count(),
        'sponsor_count' : _count(COUNT_SPONSORS),
        'programmer_count' : _count(COUNT_PROGRAMMERS),
        'paid_programmer_count' : _count(COUNT_PAID_PROGRAMMERS),
        'offer_count' : _count(COUNT_OFFERS),
        'issue_count' : _count(COUNT_ISSUES),
        'issue_project_count' : _count(COUNT_PROJECTS),
        'issue_count_kickstarting' : _count(COUNT_ISSUES_KICKSTARTING),
        'issue_count_sponsoring' : _count(COUNT_ISSUES_SPONSORING),
        'paid_offer_count' : _count(COUNT_OFFERS_PAID),
        'open_offer_count' : _count(COUNT_OFFERS_OPEN),
        'revoked_offer_count' : _count(COUNT_OFFERS_REVOKED),
        'paid_sum_usd' : _sum(SUM_PAID_USD),
        'paid_sum_btc' : _sum(SUM_PAID_BTC),
        'open_sum_usd' : _sum(SUM_OPEN_USD),
        'open_sum_btc' : _sum(SUM_OPEN_BTC),
        'expired_sum_usd' : _sum(SUM_EXPIRED_USD),
        'expired_sum_btc' : _sum(SUM_EXPIRED_BTC),
        'revoked_sum_usd' : _sum(SUM_REVOKED_USD),
        'revoked_sum_btc' : _sum(SUM_REVOKED_BTC),
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
