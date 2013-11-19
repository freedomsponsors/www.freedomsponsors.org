from frespo_currencies.models import Rates
from datetime import timedelta
from django.utils import timezone
import requests
import logging

logger = logging.getLogger(__name__)

__author__ = 'tony'

def get_rate(fron, to):
    if fron == to:
        return 1
    rates = _get_rates()
    if fron == 'USD':
        if to == 'BRL':
            return rates.usd2brl() * 1.045
        elif to == 'BTC':
            return rates._2btc('USD') * 1.02
        else:
            raise BaseException('Cannot convert %s -> %s' % (fron, to))
    elif fron == 'BTC' and to == 'BRL':
        return rates.btc2('BRL') * 1.02
    elif fron == 'BTC' and to == 'USD':
        return rates.btc2('USD') * 1.02
    else:
        raise BaseException('Cannot convert %s -> %s' % (fron, to))


def _populate_rates(rates):
    # rates.google_data = _get_google_data()
    rates.blockchain_data = _get_blockchain_data()
    rates.last_update = timezone.now()
    rates.save()


def _get_rates():
    q = Rates.objects.all()
    if q.count() > 0:
        rates = Rates.objects.all()[0]
        if timezone.now() - rates.last_update > timedelta(minutes=3):
            try:
                _populate_rates(rates)
            except BaseException, e:
                logger.error('error fetching currency rates: %s' % e)
    else:
        rates = Rates()
        _populate_rates(rates)
    return rates


def _get_google_data():
    url = 'http://www.google.com/ig/calculator?hl=en&q=1USD%3D%3FBRL'
    response = requests.get(url)
    return response.content


def _get_blockchain_data():
    response = requests.get('http://blockchain.info/pt/ticker')
    return response.content

    # def get_btc_to_usd_rate():
    #     response = requests.get('http://blockchain.info/pt/ticker')
    #     dict = json.loads(response.content)
    #     return dict['USD']['sell']
    #
    # def get_btc_to_brl_rate():
    #     response = requests.get('http://blockchain.info/pt/ticker')
    #     dict = json.loads(response.content)
    #     return dict['BRL']['sell']
