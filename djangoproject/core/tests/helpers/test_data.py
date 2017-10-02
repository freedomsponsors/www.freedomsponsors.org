from core.models import *
from bitcoin_frespo.models import *
from decimal import Decimal
from random import randint

__author__ = 'tony'

paypal_credentials_1 = {'email':'spon1_1348457115_per@gmail.com',
                        'password' : '12345678'}

def createDummyUserRandom(login, password):
    randomnum = randint(0,100000)
    random_login = '%s_%s'%(login, randomnum)
    user = User.objects.create_user(random_login, random_login+'@gogogo.com', password)
    userinfo = UserInfo.newUserInfo(user)
    userinfo.realName = login+' Real'
    userinfo.date_last_updated = timezone.now()
    userinfo.save()
    return user

def create_dummy_sponsor():
    randomnum = randint(0,100000)
    user = User.objects.create_user('userone_%s'%randomnum, 'userone_%s@gogogo.com'%randomnum, 'abcdef')
    userinfo = UserInfo.newUserInfo(user)
    userinfo.realName = 'User One'
    userinfo.date_last_updated = timezone.now()
    userinfo.save()
    return user

def create_dummy_programmer():
    randomnum = randint(0,100000)
    user = User.objects.create_user('usertwo_%s'%randomnum, 'usertwo_%s@gogogo.com'%randomnum, 'abcdef')
    userinfo = UserInfo.newUserInfo(user)
    userinfo.realName = 'User Two'
    userinfo.date_last_updated = timezone.now()
    userinfo.save()
    return user


def create_dummy_project():
    sponsor = create_dummy_sponsor()
    project = Project.newProject('Hibernate', sponsor, 'http://www.hibernate.org', 'https://hibernate.onjira.com/')
    project.save()
    return project

def create_dummy_list_project():
    sponsor = create_dummy_sponsor()
    list_projects = []
    for i in range(20):
        project = Project.newProject('Hibernate'+str(i), sponsor, 'http://www.hibernate.org', 'https://hibernate.onjira.com/')
        project.save()
        list_projects.append(project)
    return list_projects

def create_dummy_issue(project=None, key='HHH-1051', title='Compiled native SQL queries are not cached'):
    if not project:
        project = create_dummy_project()
    issue = Issue.newIssue(project, key, title, 'meh', project.createdByUser,
                           'https://hibernate.onjira.com/browse/HHH-1051')
    issue.save()
    return issue


def create_dummy_offer_usd(issue=None):
    return _create_dummy_offer_with_currency(issue, Decimal('10.00'), 'USD')


def create_dummy_offer_btc(issue=None):
    return _create_dummy_offer_with_currency(issue, Decimal('5.00'), 'BTC')


def _create_dummy_offer_with_currency(issue, value, currency):
    if not issue:
        issue = create_dummy_issue()
    offer = Offer.newOffer(issue, issue.createdByUser, value, currency, 'comita aih', True, True, None)
    offer.save()
    return offer


def create_dummy_solution(issue=None, programmer=None):
    if not issue:
        issue = create_dummy_issue()
    if not programmer:
        programmer = create_dummy_programmer()
    solution = Solution.newSolution(issue, programmer, False)
    solution.save()
    return solution


def create_dummy_payment_usd():
    offer = create_dummy_offer_usd()
    payment = Payment.newPayment(offer, offer.currency)
    payment.setPaykey('PK_ABCDEFG')
    payment.fee = Decimal('0.30')
    payment.total = Decimal('10.00')
    payment.confirm_key = 'abcd1234'
    payment.save()
    solution = create_dummy_solution()
    part = PaymentPart.newPart(payment, solution, Decimal('10.00'))
    part.save()
    return payment

def create_dummy_bitcoin_receive_address_available():
    receive_address = ReceiveAddress.newAddress('dummy_bitcoin_address_fs')
    receive_address.save()