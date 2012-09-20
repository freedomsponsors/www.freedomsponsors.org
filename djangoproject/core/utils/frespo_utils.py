from urlparse import urlparse

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

class Struct:
    def __init__(self, **entries): 
        self.__dict__.update(entries)