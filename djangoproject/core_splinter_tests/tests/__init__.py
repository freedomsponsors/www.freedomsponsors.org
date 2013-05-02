from django.conf import settings

if not settings.TEST_WITH_NOSE:
    from splintertests_issues import *
    from splintertests_users import *
    from splintertests_comments import *
    from splintertests_payment import *
