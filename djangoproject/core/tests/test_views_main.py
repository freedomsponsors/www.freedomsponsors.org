# coding: utf-8
from decimal import Decimal
from django.test import TestCase
from model_mommy import mommy


class HomeView(TestCase):
    def setUp(self):
        # Sponsoring
        for i in mommy.make_many('core.Issue', project__name='Linux', is_public_suggestion=False, quantity=11):
            mommy.make_one('core.Offer', issue=i, price=1, status='OPEN')
            mommy.make_one('core.Offer', issue=i, price=10, status='PAID')

        # Kickstarting
        for i in mommy.make_many('core.Issue', project__name='Linux', is_public_suggestion=True, quantity=11):
            mommy.make_one('core.Offer', issue=i, price=1, status='OPEN')
            mommy.make_one('core.Offer', issue=i, price=10, status='PAID')

        self.resp = self.client.get('/')

    def test_get(self):
        self.assertEquals(200, self.resp.status_code)

    def test_template(self):
        self.assertTemplateUsed(self.resp, 'core/home.html')

    def test_context(self):
        self.assertIn('issues_sponsoring', self.resp.context)
        self.assertIn('issues_kickstarting', self.resp.context)

    def test_num_queries(self):
        with self.assertNumQueries(62):
            self.client.get('/')

    def test_issues_sponsoring(self):
        sponsoring = self.resp.context['issues_sponsoring']
        expected = [(i, False, Decimal('1'), Decimal('10')) for i in range(1, 11)]

        self.assertQuerysetEqual(sponsoring, expected,
                                 lambda i: (i.pk, i.is_public_suggestion, i.getTotalOffersPrice(), i.getTotalPaidPrice()))

    def test_issues_kickstarting(self):
        sponsoring = self.resp.context['issues_kickstarting']
        expected = [(i, True) for i in range(12, 22)]

        self.assertQuerysetEqual(sponsoring, expected,
                                 lambda i: (i.pk, i.is_public_suggestion))
