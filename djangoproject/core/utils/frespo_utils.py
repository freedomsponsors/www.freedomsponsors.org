from urlparse import urlparse
from decimal import Decimal

_TWOPLACES = Decimal(10) ** -2

socialImages = {'google' : '/static/img/google.gif',
    'yahoo':'/static/img/yahoo.gif',
    'facebook':'/static/img/facebook.gif',
    'twitter':'/static/img/twitter.png',
    'github' : '/static/img/github.png',
    'bitbucket' : '/static/img/bitbucket.jpg',
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

#TODO: use this in a bunch of places (needed because sql doesn't store the .00 Decimal places - and this breaks a few tests)
def twoplaces(dec):
    return dec.quantize(_TWOPLACES)

class Struct:
    def __init__(self, **entries): 
        self.__dict__.update(entries)

