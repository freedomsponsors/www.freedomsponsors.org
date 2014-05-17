# coding: utf-8
from mock import patch, Mock
from model_mommy import mommy
from django.test import TestCase
from django.utils.datetime_safe import date
from django.core.urlresolvers import reverse as r
from core.services import stats_services


class StatsView(TestCase):
    def setUp(self):
        self.resp = self.client.get(r('stats'))

    def test_get(self):
        self.assertEqual(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'core2/stats.html')

    def test_context(self):
        self.assertIn('stats', self.resp.context)

    def test_num_queries(self):
        with self.assertNumQueries(9):
            self.client.get(r('stats'))


class Sponsors(TestCase):
    def setUp(self):
        u = mommy.make_one('core.UserInfo', screenName='sponsorA')
        mommy.make_one('core.Offer', sponsor=u.user, price=10, status='PAID', currency='USD', expirationDate=None)
        mommy.make_one('core.Offer', sponsor=u.user, price=90, status='OPEN', currency='USD', expirationDate=None)

        self.stats = stats_services.get_stats()

    def test_sponsors(self):
        qs = self.stats['sponsors']
        self.assertQuerysetEqual(qs, [('sponsorA', 2, 10, 90)],
                                 lambda u: (u.screenName, u.offer_count, u.paid_amount_usd, u.open_amount_usd))

    def test_num_queries(self):
        with self.assertNumQueries(1):
            for obj in self.stats['sponsors']:
                pass


class CountProgrammersWithSolutions(TestCase):
    def setUp(self):
        u1 = mommy.make_one('auth.User')
        u2 = mommy.make_one('auth.User')
        mommy.make_many('core.Solution', quantity=2, programmer=u1)
        mommy.make_many('core.Solution', quantity=2, programmer=u2)

        self.stats = stats_services.get_stats()

    def test_count_programmers_with_solutions(self):
        self.assertEqual(2, self.stats['programmer_count'])


class CountPaidProgrammers(TestCase):
    def setUp(self):
        mommy.make_many('core.PaymentPart', quantity=2, programmer__id=1, payment__status='CONFIRMED_IPN')
        mommy.make_many('core.PaymentPart', quantity=2, programmer__id=2, payment__status='CONFIRMED_IPN')
        mommy.make_many('core.PaymentPart', quantity=2, programmer__id=1)
        mommy.make_many('core.PaymentPart', quantity=2, programmer__id=2)
        mommy.make_many('core.PaymentPart', quantity=2, programmer__id=3)
        mommy.make_many('core.PaymentPart', quantity=2, programmer__id=4)

        self.stats = stats_services.get_stats()

    def test_count_paid_programmers(self):
        self.assertEqual(2, self.stats['paid_programmer_count'])


class Projects(TestCase):
    def setUp(self):
        for i in mommy.make_many('core.Issue', quantity=3, project__id=1, project__name='projectA'):
            mommy.make_many('core.Offer', quantity=2, price=10, issue=i)

        for i in mommy.make_many('core.Issue', quantity=2, project__id=2, project__name='projectB'):
            mommy.make_many('core.Offer', quantity=2, price=20, issue=i)

        self.stats = stats_services.get_stats()

    def test_projects(self):
        qs = self.stats['projects']
        self.assertQuerysetEqual(qs, [('projectB', 2, 4, 80), ('projectA', 3, 6, 60)],
                             lambda p: (p.name, p.issue_count, p.offer_count, p.offer_sum))


class ProjectStats(TestCase):
    def setUp(self):
        project = mommy.make_one('core.Project')
        mommy.make_one('core.Issue', project__id=project.id, status='done')
        for i in mommy.make_many('core.Issue', quantity=3, project__id=project.id, status='open'):
            mommy.make_many('core.Offer', quantity=2, price=10, issue=i, status='OPEN', currency='USD')

        self.stats = stats_services.project_stats(project)

    def test_project_stats_issues_open(self):
        self.assertEqual(self.stats['issues_open'], 3)

    def test_project_stats_issues_done(self):
        self.assertEqual(self.stats['issues_done'], 1)


class OfferStats(TestCase):
    def setUp(self):
        mommy.make_many('core.Offer', quantity=2, price=10, status='OPEN', currency='USD')
        mommy.make_many('core.Offer', quantity=2, price=11, status='PAID', currency='USD')
        mommy.make_many('core.Offer', quantity=2, price=12, status='OPEN', currency='USD', expirationDate=date.today()) #expired
        mommy.make_many('core.Offer', quantity=2, price=13, status='REVOKED', currency='USD')
        mommy.make_many('core.Offer', quantity=2, price=20, status='OPEN', currency='BTC')
        mommy.make_many('core.Offer', quantity=2, price=21, status='PAID', currency='BTC')
        mommy.make_many('core.Offer', quantity=2, price=22, status='OPEN', currency='BTC', expirationDate=date.today()) #expired
        mommy.make_many('core.Offer', quantity=2, price=23, status='REVOKED', currency='BTC')

        with self.assertNumQueries(1):
            self.stats = stats_services.get_offer_stats()

    def test_offer_count(self):
        self.assertEqual(16, self.stats['offer_count'])

    def test_sponsor_count(self):
        self.assertEqual(16, self.stats['sponsor_count'])

    def test_paid_offer_count(self):
        self.assertEqual(4, self.stats['paid_offer_count'])

    def test_open_offer_count(self):
        # FIXME: For now it's including OPEN but EXPIRED
        self.assertEqual(8, self.stats['open_offer_count'])

    def test_revoked_offer_count(self):
        self.assertEqual(4, self.stats['revoked_offer_count'])

    def test_open_sum_usd(self):
        self.assertEqual(20, self.stats['open_sum_usd'])

    def test_paid_sum_usd(self):
        self.assertEqual(22, self.stats['paid_sum_usd'])

    def test_expired_sum_usd(self):
        self.assertEqual(24, self.stats['expired_sum_usd'])

    def test_revoked_sum_usd(self):
        self.assertEqual(26, self.stats['revoked_sum_usd'])

    def test_open_sum_btc(self):
        self.assertEqual(40, self.stats['open_sum_btc'])

    def test_paid_sum_btc(self):
        self.assertEqual(42, self.stats['paid_sum_btc'])

    def test_expired_sum_btc(self):
        self.assertEqual(44, self.stats['expired_sum_btc'])

    def test_revoked_sum_btc(self):
        self.assertEqual(46, self.stats['revoked_sum_btc'])


class IssueStats(TestCase):
    def setUp(self):
        mommy.make_one('core.Issue', is_feedback=True, project__id=1)
        mommy.make_one('core.Issue', is_feedback=False, project__id=2, is_public_suggestion=False)
        mommy.make_one('core.Issue', is_feedback=False, project__id=2, is_public_suggestion=True)

        with self.assertNumQueries(1):
            self.stats = stats_services.get_issue_stats()

    def test_issue_count(self):
        self.assertEqual(2, self.stats['issue_count'])

    def test_issue_project_count(self):
        self.assertEqual(1, self.stats['issue_project_count'])

    def test_issue_count_kickstarting(self):
        self.assertEqual(1, self.stats['issue_count_kickstarting'])

    def test_issue_count_sponsoring(self):
        self.assertEqual(1, self.stats['issue_count_sponsoring'])
