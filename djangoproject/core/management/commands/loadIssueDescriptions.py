from django.core.management.base import NoArgsCommand
from optparse import make_option
from django.utils.html import strip_tags
from core.models import *
from core.utils.trackers_adapter import fetchIssueInfo
import logging
logger = logging.getLogger(__name__)


class Command(NoArgsCommand):

    help = "Populate description for issues"

    option_list = NoArgsCommand.option_list + (
        make_option('--verbose', action='store_true'),
    )
    
    def handle_noargs(self, **options):
        issues = Issue.objects.filter(description='', project__isnull=False)
        for issue in issues:
            logger.info('processing issue: %s' % issue.id)
            info = fetchIssueInfo(issue.trackerURL)
            if not info.error:
                logger.info('fetched info from: %s' % issue.trackerURL)
                issue.description = strip_tags(info.description)
                logger.info('set description: %s (...)' % issue.description[0:100])
                issue.save()
            else:
                logger.info('error fetching from: %s - %s' % (issue.trackerURL, info.error))
