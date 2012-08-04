from urlparse import urlparse

socialImages = {'google' : '/static/img/google.gif',
    'yahoo':'/static/img/yahoo.gif',
    'facebook':'/static/img/facebook.gif',
    'twitter':'/static/img/twitter.png',
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

def getUnconnectedSocialAccounts(user):
	imgs = socialImages.copy()
	for auth in user.getSocialAuths():
		del imgs[auth.provider]
	res = []
	for provider in imgs.keys():
		res.append({'provider':provider, 'icon':imgs[provider]})
	return res
    
def dictOrEmpty(dict, key):
    if(dict.has_key(key)):
        return dict[key]
    return ''

class Struct:
    def __init__(self, **entries): 
        self.__dict__.update(entries)