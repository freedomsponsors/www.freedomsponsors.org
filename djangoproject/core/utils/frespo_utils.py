from decimal import Decimal
from urlparse import urlparse


_TWOPLACES = Decimal(10) ** -2


def get_or_none(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None


#TODO: use this in a bunch of places (needed because sqlite doesn't store the .00 Decimal places - and this breaks a few tests)
def twoplaces(dec):
    return dec.quantize(_TWOPLACES)


def strip_protocol(url):
    if not url:
        return url
    elif url.startswith('http://'):
        return url[7:]
    elif url.startswith('https://'):
        return url[8:]
    else:
        return url