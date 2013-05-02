from django.conf import settings

if not settings.TEST_WITH_NOSE:
	from test_github_adapter import *
