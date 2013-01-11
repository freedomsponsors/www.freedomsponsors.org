from urlparse import urlparse
from decimal import Decimal
from django.core.mail import EmailMultiAlternatives
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)

_TWOPLACES = Decimal(10) ** -2

socialImages = {'google' : '/static/img/google.gif',
    'yahoo':'/static/img/yahoo.gif',
    'facebook':'/static/img/facebook.gif',
    'twitter':'/static/img/twitter.png',
    'github' : '/static/img/github.png',
    'bitbucket' : '/static/img/bitbucket.jpg',
#    'myopenid' : '/static/img/myopenid.png'
}

socialImages_small = {'google' : '/static/img/google_small.png',
    'yahoo':'/static/img/yahoo_small.png',
    'facebook':'/static/img/facebook_small.png',
    'twitter':'/static/img/twitter_small.png',
    'github' : '/static/img/github_small.gif',
    'bitbucket' : '/static/img/bitbucket_small.png',
#    'myopenid' : '/static/img/myopenid.png'
}

def validateIssueURL(url):
    parsedURL = urlparse(url)
    if(not parsedURL.scheme == 'http' and not parsedURL.scheme == 'https'):
        return 'protocol must be http or https'
    elif(not parsedURL.path or parsedURL.path == '/'):
        return 'This is not a issue URL'
    else:
        return ''

def validateURL(url):
    parsedURL = urlparse(url)
    if(not parsedURL.scheme == 'http' and not parsedURL.scheme == 'https'):
        return 'protocol must be http or https'
    elif(not parsedURL.netloc or parsedURL.netloc.find('.') < 0 ):
        return 'invalid URL'
    else:
        return ''

def get_or_none(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None


def dictOrEmpty(dict, key):
    if(dict.has_key(key)):
        return dict[key]
    return ''

def send_html_mail(subject, body_txt, body_html, from_email, to_addresses):
    try:
        for to_addr in to_addresses:
            validate_email(to_addr)
    except ValidationError:
        logger.warn('Email not sent. Invalid email address in %s. subject = %s' % (to_addresses, subject))
        return
    msg = EmailMultiAlternatives(subject, body_txt, from_email, to_addresses)
    msg.attach_alternative(body_html, "text/html")
    msg.send()

#TODO: use this in a bunch of places (needed because sqlite doesn't store the .00 Decimal places - and this breaks a few tests)
def twoplaces(dec):
    return dec.quantize(_TWOPLACES)

class Struct:
    def __init__(self, **entries): 
        self.__dict__.update(entries)

