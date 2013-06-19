from decimal import Decimal
from django.conf import settings
from django.template import loader
from django.template.context import Context
from core.services import mail_services

__author__ = 'tony'


SPONSOR = {
    'getUserInfo': {
        'screenName': 'Mr Sponsor'
    }
}


PAYMENT_BITCOIN = {
    'total_bitcoin_received': Decimal('10.30'),
    'parts': [
        {
            'solution': {
                'programmer': {
                    'getUserInfo': {
                        'screenName': 'Programmer 1'
                    }
                },
            },
            'money_sent': {
                'value': Decimal('6.00'),
                'transaction_hash': 'dadadadadadadadadaddadadadadadadadada'
            }
        },
        {
            'solution': {
                'programmer': {
                    'getUserInfo': {
                        'screenName': 'Programmer 2'
                    }
                },
            },
            'money_sent': {
                'value': Decimal('4.00'),
                'transaction_hash': 'bebebebebebebebebebebebebebebebebebeb'
            }
        }
    ]
}


def testmail(test, to):
    if test == 'bitcoin_payment_was_sent_to_programmers_and_is_waiting_confirmation':
        template = loader.get_template('email/bitcoin_payment_was_sent_to_programmers_and_is_waiting_confirmation.html')
        contextData = {
            'you': SPONSOR,
            'payment': PAYMENT_BITCOIN,
            'parts': PAYMENT_BITCOIN['parts']
        }
        context = Context(contextData)
        html_content = template.render(context)
        subject = 'BTC %s payment received, and forwarded to programmer. Wating confirmation.'
        mail_services.send_html_mail(subject, html_content, html_content, settings.DEFAULT_FROM_EMAIL, [to])
    else:
        raise BaseException('unknown mail test: %s' % test)
