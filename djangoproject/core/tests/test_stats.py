# coding: utf-8
from mock import patch, Mock
from model_mommy import mommy
from django.test import TestCase
from django.utils.datetime_safe import date
from core.services import stats_services


class StatsView(TestCase):
    def setUp(self):
        self.resp = self.client.get('/core/stats/')

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'core/stats.html')

    def test_context(self):
        self.assertIn('stats', self.resp.context)

    def test_num_queries(self):
        with self.assertNumQueries(18):
            self.client.get('/core/stats/')


class CountProject(TestCase):
    def setUp(self):
        mommy.make_one('core.Project')

        p = mommy.make_one('core.Project')
        mommy.make_one('core.Issue', project=p, createdByUser=p.createdByUser, is_feedback=False)
        mommy.make_one('core.Issue', project=p, createdByUser=p.createdByUser, is_feedback=False)
        mommy.make_one('core.Issue', project=p, createdByUser=p.createdByUser, is_feedback=True)

        self.stats = stats_services.get_stats()

    def test_count_project(self):
        self.assertEqual(1, self.stats['issue_project_count'])


class CountKickstarting(TestCase):
    def setUp(self):
        mommy.make_one('core.Issue', is_feedback=False, is_public_suggestion=False)
        mommy.make_one('core.Issue', is_feedback=True, is_public_suggestion=False)
        mommy.make_one('core.Issue', is_feedback=True, is_public_suggestion=True)

        # Query hit
        mommy.make_many('core.Issue', quantity=2, is_feedback=False, is_public_suggestion=True)

        self.stats = stats_services.get_stats()

    def test_count_kickstarting(self):
        self.assertEqual(2, self.stats['issue_count_kickstarting'])

class CountSponsoring(TestCase):
    def setUp(self):
        mommy.make_one('core.Issue', is_feedback=False, is_public_suggestion=True)
        mommy.make_one('core.Issue', is_feedback=True, is_public_suggestion=False)
        mommy.make_one('core.Issue', is_feedback=True, is_public_suggestion=True)

        # Query hit
        mommy.make_many('core.Issue', quantity=2, is_feedback=False, is_public_suggestion=False)

        self.stats = stats_services.get_stats()

    def test_count_sponsoring(self):
        self.assertEqual(2, self.stats['issue_count_sponsoring'])


class SumPriceOfOpenOffers(TestCase):
    def setUp(self):
        mommy.make_one('core.Offer', status='PAID', price=1, expirationDate=None)
        mommy.make_one('core.Offer', status='PAID', price=1, expirationDate=date(2012, 12, 12))
        mommy.make_one('core.Offer', status='PAID', price=1, expirationDate=date(2012, 12, 13))
        mommy.make_one('core.Offer', status='PAID', price=1, expirationDate=date(2012, 12, 01))
        mommy.make_one('core.Offer', status='OPEN', price=1, expirationDate=date(2012, 12, 01))
        mommy.make_one('core.Offer', status='OPEN', price=1, expirationDate=date(2012, 12, 12))
        # Query hits
        mommy.make_one('core.Offer', status='OPEN', price=9, expirationDate=None)
        mommy.make_one('core.Offer', status='OPEN', price=90, expirationDate=date(2012, 12, 13))

        with patch('django.utils.datetime_safe.date.today', Mock(return_value=date(2012, 12, 12))):
            self.stats = stats_services.get_stats()

    def test_sum_price_of_open_offers(self):
        self.assertEqual(99, self.stats['open_sum'])


class SumPriceOfExpiredOffers(TestCase):
    def setUp(self):
        mommy.make_one('core.Offer', status='PAID', price=1, expirationDate=None)
        mommy.make_one('core.Offer', status='PAID', price=1, expirationDate=date(2012, 12, 12))
        mommy.make_one('core.Offer', status='PAID', price=1, expirationDate=date(2012, 12, 13))
        mommy.make_one('core.Offer', status='PAID', price=1, expirationDate=date(2012, 12, 01))
        mommy.make_one('core.Offer', status='OPEN', price=1, expirationDate=None)
        mommy.make_one('core.Offer', status='OPEN', price=1, expirationDate=date(2012, 12, 13))

        # Query hits
        mommy.make_one('core.Offer', status='OPEN', price=9, expirationDate=date(2012, 12, 01))
        mommy.make_one('core.Offer', status='OPEN', price=90, expirationDate=date(2012, 12, 12))

        with patch('django.utils.datetime_safe.date.today', Mock(return_value=date(2012, 12, 12))):
            self.stats = stats_services.get_stats()

    def test_sum_price_of_expired_offers(self):
        self.assertEqual(99, self.stats['expired_sum'])


class Sponsors(TestCase):
    def setUp(self):
        u = mommy.make_one('core.UserInfo', screenName='sponsorA')
        mommy.make_one('core.Offer', sponsor=u.user, price=10, status='PAID', expirationDate=None)
        mommy.make_one('core.Offer', sponsor=u.user, price=90, status='OPEN', expirationDate=None)

        self.stats = stats_services.get_stats()

    def test_sponsors(self):
        qs = self.stats['sponsors']
        self.assertQuerysetEqual(qs, [('sponsorA', 10, 90)],
                                 lambda u: (u.screenName, u.paid_ammount, u.open_ammount))


