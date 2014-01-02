from decimal import Decimal
from datetime import timedelta
from django.utils import timezone


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


def as_time_string(date):
    delta = timezone.now() - date
    five_secs = timedelta(seconds=5)
    one_minute = timedelta(seconds=60)
    one_hour = timedelta(hours=1)
    one_day = timedelta(days=1)
    one_month = timedelta(days=30)
    if delta < five_secs:
        return 'just now'
    elif delta < one_minute:
        return '%s seconds ago' % delta.seconds
    elif delta < one_hour:
        m = int(delta.seconds / 60)
        return '%s minutes ago' % m
    elif delta < one_day:
        h = int(delta.seconds / 3600)
        return '%s hours ago' % h
    elif delta < one_month:
        return '%s days ago' % delta.days
    else:
        return date.strftime('on %Y/%m/%d')