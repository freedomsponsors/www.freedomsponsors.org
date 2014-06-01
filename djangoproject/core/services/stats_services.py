from datetime import datetime
from core.models import *
from django.db import connection
import math
from frespo_currencies import currency_service

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

COUNT_ISSUES_SPONSORING_OPEN_OR_WORKING_BY_PROJECT = """select count(*) from core_issue i
where i.project_id = %s
and i.status in ('open', 'working')
and i.is_feedback = false
and i.is_public_suggestion = false"""
COUNT_ISSUES_SPONSORING_DONE_BY_PROJECT = """select count(*) from core_issue i
where i.project_id = %s
and i.status = 'done'"""


SUM_PAID_USD = "select sum (price) from core_offer where status = 'PAID' and currency = 'USD'"
SUM_PAID_BTC = "select sum (price) from core_offer where status = 'PAID' and currency = 'BTC'"

SUM_OPEN_USD = """select sum (price) from core_offer where status = 'OPEN' and currency = 'USD' and ("expirationDate" is null or "expirationDate" > now())"""
SUM_OPEN_BTC = """select sum (price) from core_offer where status = 'OPEN' and currency = 'BTC' and ("expirationDate" is null or "expirationDate" > now())"""

SUM_PAID_USD_BY_PROJECT = """select sum (o.price) from core_offer o, core_issue i
where i.project_id = %s
and i.id = o.issue_id
and o.status = 'PAID'
and o.currency = 'USD'"""
SUM_PAID_BTC_BY_PROJECT = """select sum (o.price) from core_offer o, core_issue i
where i.project_id = %s
and i.id = o.issue_id
and o.status = 'PAID'
and o.currency = 'BTC'"""

SUM_OPEN_USD_BY_PROJECT = """select sum (o.price) from core_offer o, core_issue i
where i.project_id = %s
and i.id = o.issue_id
and o.status = 'OPEN'
and o.currency = 'USD'
and (o."expirationDate" is null or o."expirationDate" > now())"""
SUM_OPEN_BTC_BY_PROJECT = """select sum (o.price) from core_offer o, core_issue i
where i.project_id = %s
and i.id = o.issue_id
and o.status = 'OPEN'
and o.currency = 'BTC'
and (o."expirationDate" is null or o."expirationDate" > now())"""


SUM_EXPIRED_USD = """select sum (price) from core_offer where status = 'OPEN' and currency = 'USD' and "expirationDate" <= now()"""
SUM_EXPIRED_BTC = """select sum (price) from core_offer where status = 'OPEN' and currency = 'BTC' and "expirationDate" <= now()"""

SUM_REVOKED_USD = "select sum (price) from core_offer where status = 'REVOKED' and currency = 'USD'"
SUM_REVOKED_BTC = "select sum (price) from core_offer where status = 'REVOKED' and currency = 'BTC'"

LAUNCH_DATE = datetime(2012, 7, 8)


def get_stats():
    btc2usd = currency_service.get_rate('BTC', 'USD', False)
    btc2usd_decimal = Decimal(str(btc2usd))

    open_sum_btc        = _sum(SUM_OPEN_BTC)
    open_sum_btc_in_usd = open_sum_btc * btc2usd_decimal

    paid_sum_btc        = _sum(SUM_PAID_BTC)
    paid_sum_btc_in_usd = paid_sum_btc * btc2usd_decimal

    revoked_sum_btc        =  _sum(SUM_REVOKED_BTC)
    revoked_sum_btc_in_usd = revoked_sum_btc * btc2usd_decimal

    expired_sum_btc        =  _sum(SUM_EXPIRED_BTC)
    expired_sum_btc_in_usd = expired_sum_btc * btc2usd_decimal

    return {
        'age': _age(),
        'user_count': UserInfo.objects.count(),
        'sponsor_count': _count(COUNT_SPONSORS),
        'programmer_count': _count(COUNT_PROGRAMMERS),
        'paid_programmer_count': _count(COUNT_PAID_PROGRAMMERS),
        'offer_count': _count(COUNT_OFFERS),
        'issue_count': _count(COUNT_ISSUES),
        'issue_project_count': _count(COUNT_PROJECTS),
        'issue_count_kickstarting': _count(COUNT_ISSUES_KICKSTARTING),
        'issue_count_sponsoring': _count(COUNT_ISSUES_SPONSORING),
        'paid_offer_count': _count(COUNT_OFFERS_PAID),
        'open_offer_count': _count(COUNT_OFFERS_OPEN),
        'revoked_offer_count': _count(COUNT_OFFERS_REVOKED),
        'paid_sum_usd': _sum(SUM_PAID_USD),
        'paid_sum_btc': paid_sum_btc,
        'paid_sum_btc_in_usd': paid_sum_btc_in_usd,
        'open_sum_usd': _sum(SUM_OPEN_USD),
        'open_sum_btc': open_sum_btc,
        'open_sum_btc_in_usd': open_sum_btc_in_usd,
        'expired_sum_usd': _sum(SUM_EXPIRED_USD),
        'expired_sum_btc': expired_sum_btc,
        'expired_sum_btc_in_usd': expired_sum_btc_in_usd,
        'revoked_sum_usd': _sum(SUM_REVOKED_USD),
        'revoked_sum_btc': revoked_sum_btc,
        'revoked_sum_btc_in_usd': revoked_sum_btc_in_usd,
        'sponsors': _select(SELECT_SPONSORS),
        'projects': _select(SELECT_SPONSORED_PROJECTS),
    }


def _age():
    delta = (datetime.today() - LAUNCH_DATE).days
    years, days = divmod(delta, 365)
    months = int(days/30.5)
    s = "%d %s" % (years, 'year' if years == 1 else 'years')
    if months > 0:
        s += " and %d %s" % (months, 'month' if months == 1 else 'months')
    return s;


def _count(query, params=None):
    return int(_sum(query, params))


def _sum(query, params=None):
    rows = _select(query, params)
    r = rows[0][0]
    if r is None:
        r = 0
    return r


def _select(query, params=None):
    if not params:
        params = []
    cursor = connection.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    return rows


def project_stats(project):
    id = project.id
    issues_open = _count(COUNT_ISSUES_SPONSORING_OPEN_OR_WORKING_BY_PROJECT, [id])
    issues_done = _count(COUNT_ISSUES_SPONSORING_DONE_BY_PROJECT, [id])
    usd_paid = _sum(SUM_PAID_USD_BY_PROJECT, [id])
    usd_open = _sum(SUM_OPEN_USD_BY_PROJECT, [id])
    btc_paid = _sum(SUM_PAID_BTC_BY_PROJECT, [id])
    btc_open = _sum(SUM_OPEN_BTC_BY_PROJECT, [id])
    total_issues = issues_open + issues_done
    total_usd = usd_open + usd_paid
    total_btc = btc_open + btc_paid
    result = {
        'issues_open': issues_open,
        'issues_done': issues_done,
        'usd_paid': usd_paid,
        'usd_open': usd_open,
        'btc_paid': btc_paid,
        'btc_open': btc_open,
        'total_issues': total_issues,
        'total_usd': total_usd,
        'total_btc': total_btc,
    }
    if total_issues > 0:
        percent_issues_open = int(100 * issues_open / total_issues)
        percent_issues_done = int(100 * issues_done / total_issues)
        result.update({
            'percent_issues_open': percent_issues_open,
            'percent_issues_done': percent_issues_done,
        })
    if total_usd > 0:
        percent_usd_paid = int(100 * usd_paid / total_usd)
        percent_usd_open = int(100 * usd_open / total_usd)
        result.update({
            'percent_usd_paid': percent_usd_paid,
            'percent_usd_open': percent_usd_open,
        })
    if total_btc > 0:
        percent_btc_paid = int(100 * btc_paid / total_btc)
        percent_btc_open = int(100 * btc_open / total_btc)
        result.update({
            'percent_btc_paid': percent_btc_paid,
            'percent_btc_open': percent_btc_open,
        })
    return result


def project_top_sponsors(project_id):
    btc2usd = currency_service.get_rate('BTC', 'USD', False)
    SIZE = 10
    query = Payment.objects.select_related('offer__sponsor').filter(
        offer__issue__project__id=project_id,
        status__in=[Payment.CONFIRMED_IPN, Payment.CONFIRMED_TRN]).extra(
        {'total_usd': 'total / usd2payment_rate'}).order_by('-total_usd')
    sponsors = {}
    for payment in query:
        sponsor_id = payment.offer.sponsor.id
        sponsor = sponsors.get(sponsor_id)
        if not sponsor:
            sponsor = payment.offer.sponsor
            sponsors[sponsor_id] = payment.offer.sponsor
        if not hasattr(sponsor, 'paid_usd'):
            setattr(sponsor, 'paid_usd', Decimal(0))
        sponsor.paid_usd += payment.total_usd
        if len(sponsors) >= SIZE:
            break
    if len(sponsors) < SIZE:
        usd_offers = Offer.objects.select_related('sponsor').filter(
            issue__project_id=project_id,
            status=Offer.OPEN,
            currency='USD'
        ).order_by('-price')
        btc_offers = Offer.objects.select_related('sponsor').filter(
            issue__project_id=project_id,
            status=Offer.OPEN,
            currency='BTC'
        ).order_by('-price')
        def map_offer_sponsor(offer):
            sponsor_id = offer.sponsor.id
            sponsor = sponsors.get(sponsor_id)
            if not sponsor:
                sponsor = offer.sponsor
                sponsors[sponsor_id] = sponsor
            if not hasattr(sponsor, 'offered_usd'):
                setattr(sponsor, 'offered_usd', Decimal(0))
            offered_usd = offer.price
            if offer.currency == 'BTC':
                offered_usd *= Decimal(str(btc2usd))
            sponsor.offered_usd += offered_usd
        for offer_usd in usd_offers[0:10]:
            map_offer_sponsor(offer_usd)
        for offer_btc in btc_offers[0:10]:
            map_offer_sponsor(offer_btc)
        # for offer_usd, offer_btc in zip(usd_offers, btc_offers):
        #     map_offer_sponsor(offer_usd)
        #     map_offer_sponsor(offer_btc)
        #     if len(sponsors) >= SIZE:
        #         break
    for sponsor in sponsors.values():
        if not hasattr(sponsor, 'paid_usd'):
            setattr(sponsor, 'paid_usd', Decimal(0))
        if not hasattr(sponsor, 'offered_usd'):
            setattr(sponsor, 'offered_usd', Decimal(0))
    def compare_sponsors(s1, s2):
        dif = s1.paid_usd - s2.paid_usd
        if dif != 0:
            return int(math.copysign(1, dif))
        dif = s1.offered_usd - s2.offered_usd
        if dif != 0:
            return int(math.copysign(1, dif))
        return 0
    sponsors = sorted(sponsors.values(), compare_sponsors, reverse=True)
    return sponsors


def project_top_programmers(project_id):
    btc2usd = currency_service.get_rate('BTC', 'USD', False)
    SIZE = 10
    parts_usd = PaymentPart.objects.select_related('programmer', 'payment').filter(
        payment__offer__issue__project__id=project_id,
        payment__status__in=[Payment.CONFIRMED_IPN, Payment.CONFIRMED_TRN],
        payment__currency='USD').order_by('-price')
    parts_btc = PaymentPart.objects.select_related('programmer', 'payment').filter(
        payment__offer__issue__project__id=project_id,
        payment__status__in=[Payment.CONFIRMED_IPN, Payment.CONFIRMED_TRN],
        payment__currency='BTC').order_by('-price')
    programmers = {}
    def map_part(part):
        programmer_id = part.programmer.id
        programmer = programmers.get(programmer_id)
        if not programmer:
            programmer = part.programmer
            programmers[programmer_id] = programmer
        if not hasattr(programmer, 'received_usd'):
            setattr(programmer, 'received_usd', Decimal(0))
        received_usd = part.price
        if part.payment.currency == 'BTC':
            received_usd *= Decimal(str(btc2usd))
        programmer.received_usd += received_usd
    for part_usd in parts_usd[0:10]:
        map_part(part_usd)
    for part_btc in parts_btc[0:10]:
        map_part(part_btc)
    # for part_usd, part_btc in zip(parts_usd, parts_btc):
    #     map_part(part_usd)
    #     map_part(part_btc)
    #     if len(programmers) > SIZE:
    #         break
    def add_solution(solution):
        programmer_id = solution.programmer.id
        programmer = programmers.get(programmer_id)
        if not programmer:
            programmer = solution.programmer
            programmers[programmer_id] = programmer
        if solution.status == Solution.DONE:
            if not hasattr(programmer, 'done'):
                setattr(programmer, 'done', 0)
            programmer.done += 1
    if len(programmers) < SIZE:
        solutions_done = Solution.objects.select_related('programmer').filter(
            issue__project__id=project_id,
            status=Solution.DONE
        ).order_by('-lastChangeDate')
        for solution in solutions_done:
            add_solution(solution)
            if len(programmers) > SIZE:
                break
    if len(programmers) < SIZE:
        solutions_open = Solution.objects.select_related('programmer').filter(
            issue__project__id=project_id,
            status=Solution.IN_PROGRESS
        ).order_by('-lastChangeDate')
        for solution in solutions_open:
            add_solution(solution)
            if len(programmers) > SIZE:
                break
    for programmer in programmers.values():
        if not hasattr(programmer, 'received_usd'):
            setattr(programmer, 'received_usd', Decimal(0))
        if not hasattr(programmer, 'done'):
            setattr(programmer, 'done', 0)
    def compare_programmers(s1, s2):
        dif = s1.received_usd - s2.received_usd
        if dif != 0:
            return int(math.copysign(1, dif))
        dif = s1.done - s2.done
        if dif != 0:
            return int(math.copysign(1, dif))
        return 0
    programmers = sorted(programmers.values(), compare_programmers, reverse=True)
    return programmers
