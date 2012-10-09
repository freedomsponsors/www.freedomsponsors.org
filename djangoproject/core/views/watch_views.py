# Create your views here.

from core.models import *
from django.http import HttpResponse
from core.utils.frespo_utils import  dictOrEmpty
import json
from core.services import issue_services
import traceback
import logging

logger = logging.getLogger(__name__)

def watchIssue(request, issue_id):
    pass

def unwatchIssue(request, issue_id):
    pass

def watchOffer(request, offer_id):
    pass

def unwatchOffer(request, offer_id):
    pass

