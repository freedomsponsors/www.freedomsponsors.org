from frespo_currencies.models import Rates
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
import requests
import logging

logger = logging.getLogger(__name__)

__author__ = 'tony'


def get_rate(fron, to, for_payment=True):
    if fron == to:
        return 1
    rates = _get_rates()
    if fron == 'USD':
        if to == 'BRL':
            r = rates.usd2brl()
            if for_payment:
                r *= 1.045
            return r
        elif to == 'BTC':
            r = rates._2btc('USD')
            if for_payment:
                r *= 1.02
            return r
        else:
            raise BaseException('Cannot convert %s -> %s' % (fron, to))
    elif fron == 'BTC' and to == 'BRL':
        btc2usd = rates.btc2('USD')
        usd2brl = rates.usd2brl()
        r = btc2usd * usd2brl
        if for_payment:
            r *= 1.02
        return r
    elif fron == 'BTC' and to == 'USD':
        r = rates.btc2('USD')
        if for_payment:
            r *= 1.02
        return r
    else:
        raise BaseException('Cannot convert %s -> %s' % (fron, to))


def _get_rates():
    q = Rates.objects.all()
    if q.count() > 0:
        rates = Rates.objects.all()[0]
        if timezone.now() - rates.last_update_blockchain > timedelta(minutes=3):
            _get_blockchain_data(rates)
        if timezone.now() - rates.last_update_oer > timedelta(minutes=240):
            _get_oer_data(rates)
    else:
        rates = Rates.create_empty()
        _get_blockchain_data(rates)
        _get_oer_data(rates)
    return rates


def _get_blockchain_data(rates):
    response = requests.get('http://blockchain.info/pt/ticker')
    content = response.content
    if Rates.is_valid_blockchain_data(content):
        rates.blockchain_data = content
        rates.last_update_blockchain = timezone.now()
        rates.save()
    else:
        logger.error('got invalid Blockchain data: %s' % content)


def _get_oer_data(rates):
    response = requests.get('http://openexchangerates.org/api/latest.json?app_id=%s' % settings.OPENEXCHANGERATES_API_KEY)
    content = response.content
    if Rates.is_valid_oer_data(content):
        rates.oer_data = content
        rates.last_update_oer = timezone.now()
        rates.save()
    else:
        logger.error('got invalid OpenExchangeRate data: %s' % content)

