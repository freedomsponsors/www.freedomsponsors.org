from urlparse import urlparse
from decimal import Decimal

_TWOPLACES = Decimal(10) ** -2

CURRENCY_SYMBOLS = {'USD' : 'US$',
    'BRL' : 'R$',
    'BTC' : 'BTC'}

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

#TODO: use this in a bunch of places (needed because sqlite doesn't store the .00 Decimal places - and this breaks a few tests)
def twoplaces(dec):
    return dec.quantize(_TWOPLACES)

class Struct:
    def __init__(self, **entries): 
        self.__dict__.update(entries)

