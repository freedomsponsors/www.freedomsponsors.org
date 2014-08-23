from django.contrib.auth.models import User
from django.test import TestCase
from core.models import Watch, Offer, Solution
from core.services import watch_services, user_services
from core.tests.helpers import test_data


class TestUserServices(TestCase):
    def test_deactivated_user_should_not_be_sponsoring_working_or_watching(self):
        offer = test_data.create_dummy_offer_btc()
        user = offer.sponsor
        solution = test_data.create_dummy_solution(programmer=user)
        issue = test_data.create_dummy_issue()
        watch_services.toggle_watch(user, 'ISSUE', issue.id, Watch.WATCHED)
        
        user = User.objects.get(pk=user.id)
        offer = Offer.objects.get(pk=offer.id)
        solution = Solution.objects.get(pk=solution.id)
        self.assertTrue(user.is_active)
        self.assertEqual(Offer.OPEN, offer.status)
        self.assertEqual(Solution.IN_PROGRESS, solution.status)
        self.assertTrue(watch_services.is_watching_issue(user, issue.id))

        user_services.deactivate_user(user)

        user = User.objects.get(pk=user.id)
        offer = Offer.objects.get(pk=offer.id)
        solution = Solution.objects.get(pk=solution.id)
        self.assertFalse(user.is_active)
        self.assertEqual(Offer.REVOKED, offer.status)
        self.assertEqual(Solution.ABORTED, solution.status)
        self.assertFalse(watch_services.is_watching_issue(user, issue.id))
        self.assertFalse(watch_services.is_watching_project(user, issue.project.id))
        self.assertFalse(watch_services.is_watching_issue(user, offer.issue.id))
        self.assertFalse(watch_services.is_watching_issue(user, solution.issue.id))
