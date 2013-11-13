__author__ = 'tony'
from django.shortcuts import render_to_response
from django.template import RequestContext
from datetime import datetime
import json


def home(request):
    issues_kickstarting = [
        {"status": "open", "viewcount": -1, "four_sponsors": [], "description": "Hi, I usually contribute patches to different gnome projects, all gnome projects host their bugs on bugzilla.gnome.org, so I would like to have a way to list/search all issues whose \'original issue\' link point to some bugzilla.gnome.org bug.I think this is a very interesting feature, because every bugzilla (kde bugzilla, mozilla bugzilla, eclipse bugzilla) refer to an ecosystem of interconnected projects where a developer usually touches several of them, and so, it would want to find issues to solve in projects that belong to that bugzilla ecosystem.  ", "project_link": "/core/issue/?s=&project_id=1&project_name=www.freedomsponsors.org", "image_link": "/static/media/project_images/image3x1_1_20130711021828.png", "sponsor_status": "PROPOSED", "totalOffersPriceUSD": "0.00", "totalOffersPriceBTC": "0.00", "moresponsors": 0, "id": 19, "title": "[FEATURE REQUEST] Possibility to list/search issues by bug tracker", "totalPaidPriceUSD": "0.00", "commentcount": 0},
        {"status": "open", "viewcount": -1, "four_sponsors": [], "description": "Uma issue com um titulo que era muito grande porque o tony ficou digitando sem parar pra ver se o texto ficava com reticencias na hora mostrasse no cartaozinho da home.\\nAtirei o pau no gato mas o gato nao morreu. \\nDona Chica ca admirou-se-se do berr\\u00f4 do berr\\u00f4 que o gato deuMIAU", "project_link": "#", "image_link": "", "sponsor_status": "PROPOSED", "totalOffersPriceUSD": "0.00", "moresponsors": 0, "id": 17, "title": "Outra issue com um titulo que era muito grande porque o tony ficou digitando sem parar pra ver se o texto ficava com reticencias na hora mostrasse no cartaozinho da home", "totalPaidPriceUSD": "0.00", "commentcount": 0},
        {"status": "open", "viewcount": -1, "four_sponsors": [], "description": "Criar CSS para as janelas Modal do Freedom Sponsors", "project_link": "/core/issue/?s=&project_id=1&project_name=www.freedomsponsors.org", "image_link": "/static/media/project_images/image3x1_1_20130711021828.png", "sponsor_status": "PROPOSED", "totalOffersPriceUSD": "0.00", "moresponsors": 0, "id": 12, "title": "CSS Modal", "totalPaidPriceUSD": "0.00", "commentcount": 0}
    ]
    issues_sponsoring = [
        {"status": "open", "viewcount": -1, "four_sponsors": [{"image_link": "http://www.gravatar.com/avatar/4dbc40e7a6fa89a3568a926378c22ace?d=identicon&s=50", "screen_name": "TonyFran\\u00e7a"}], "description": "Remove all dependencies described in https://github.com/freedomsponsors/www.freedomsponsors.org/issues/146, except django-registration.", "project_link": "/core/issue/?s=&project_id=1&project_name=www.freedomsponsors.org", "image_link": "/static/media/project_images/image3x1_1_20130711021828.png", "sponsor_status": "SPONSORED", "totalOffersPriceUSD": "32.00", "totalOffersPriceBTC": "0.00", "moresponsors": 0, "id": 23, "title": "Remove dependencies", "totalPaidPriceUSD": "0.00", "totalPaidPriceBTC": "0.00", "commentcount": 0},
        {"status": "open", "viewcount": -1, "four_sponsors": [{"image_link": "http://www.gravatar.com/avatar/4dbc40e7a6fa89a3568a926378c22ace?d=identicon&s=50", "screen_name": "TonyFran\\u00e7a"}], "description": "", "project_link": "/core/issue/?s=&project_id=1&project_name=www.freedomsponsors.org", "image_link": "/static/media/project_images/image3x1_1_20130711021828.png", "sponsor_status": "SPONSORED", "totalOffersPriceUSD": "12.00", "totalOffersPriceBTC": "0.00", "moresponsors": 0, "id": 22, "title": "Google error", "totalPaidPriceUSD": "0.00", "totalPaidPriceBTC": "0.00", "commentcount": 0},
        {"status": "open", "viewcount": -1, "four_sponsors": [{"image_link": "http://www.gravatar.com/avatar/4dbc40e7a6fa89a3568a926378c22ace?d=identicon&s=50", "screen_name": "TonyFran\\u00e7a"}], "description": "atirei o pau no gato", "project_link": "/core/issue/?s=&project_id=1&project_name=www.freedomsponsors.org", "image_link": "/static/media/project_images/image3x1_1_20130711021828.png", "sponsor_status": "SPONSORED", "totalOffersPriceUSD": "32.00", "totalOffersPriceBTC": "0.00", "moresponsors": 0, "id": 21, "title": "blaublau", "totalPaidPriceUSD": "0.00", "totalPaidPriceBTC": "0.00", "commentcount": 0}
    ]
    context = {
        'issues_kickstarting': json.dumps(issues_kickstarting),
        'issues_sponsoring': json.dumps(issues_sponsoring),
        'crumbs': [{'link': '/', 'name': 'Home'}],
        'sandbox': True,
    }
    return render_to_response('core2/home.html',
        context, context_instance=RequestContext(request))


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
