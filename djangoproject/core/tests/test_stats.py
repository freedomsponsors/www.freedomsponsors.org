# coding: utf-8
from model_mommy import mommy
from django.test import TestCase
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


