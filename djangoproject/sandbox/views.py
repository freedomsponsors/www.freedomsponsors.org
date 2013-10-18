__author__ = 'tony'
from django.shortcuts import render_to_response
from django.template import RequestContext
from datetime import datetime


def issue(request):
    _crumbs = [{
        'link': '/',
        'name': 'Home'
    },
    {
        'link': '#',
        'name': 'issue: ' + 'Build a time machine'
    }]
    _actionbar = {
        'sponsor': True,
        'work': True,
        'pay': False,
        'change': False,
        'revoke': False,
        'resolve': False,
        'abort': False,
    }
    _issue = {
        'createdByUser': {'id': 1},
        'description': 'Bla\nble',
        'title': 'Build a time machine',
        'project': {'name': 'Impossibilities'},
        'get_card_image': '/static/img2/github_logo.jpg',
        'getTotalOffersPriceUSD': 120.00,
        'getTotalPaidPriceUSD': 30.00,
        'getTotalPaidPriceBTC': 0.45,
        'get_status': 'open',
        'getComments': [
            {'id': 1, 'content': 'Hey', 'author': {'id': 1}},
            {'id': 2, 'content': 'Hoo'},
        ],
        'getOffers':[
            {
             'id': 1,
             'sponsor': {'getUserInfo': {'screenName': 'Demi Moore'}},
             'get_currency_symbol': 'US$',
             'price_2': '60.00',
             'no_forking': True,
             'require_release': True,
             'status': 'OPEN',
             'creationDate': datetime.now(),
            },
            {
             'id': 2,
             'sponsor': {'getUserInfo': {'screenName': 'Johnny Depp'}},
             'get_currency_symbol': 'BTC',
             'price_2': '3.00',
             'no_forking': True,
             'require_release': True,
             'status': 'OPEN',
             'creationDate': datetime.now(),
             },
        ],
        'getSolutions': [
            {'programmer': {'getUserInfo': {'screenName': 'Nicholas Cage'}},
             'status': 'DONE',
             'accepting_payments': True,
             'creationDate': datetime.now()}
        ],
    }
    _user = {'id': 1}

    context = {
        'issue': _issue,
        'is_watching': False,
        'myoffer': None,
        'mysolution': None,
        'invoke_parent_callback': None,
        'show_sponsor_popup': None,
        'show_alert': None,
        'alert_reputation_revoking': None,
        'crumbs': _crumbs,
        'actionbar': _actionbar,
        'user': _user}
    return render_to_response('core2/issue.html',
                              context, context_instance=RequestContext(request))
