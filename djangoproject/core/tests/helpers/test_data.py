from core.models import *
from decimal import Decimal
from random import randint

__author__ = 'tony'

def createDummyUserRandom(login, password):
    randomnum = randint(0,100000)
    random_login = '%s_%s'%(login, randomnum)
    user = User.objects.create_user(random_login, random_login+'@gogogo.com', password)
    userinfo = UserInfo.newUserInfo(user)
    userinfo.screenName = login+' Screen'
    userinfo.realName = login+' Real'
    userinfo.save()
    return user

def create_dummy_sponsor():
    randomnum = randint(0,100000)
    user = User.objects.create_user('userone_%s'%randomnum, 'userone_%s@gogogo.com'%randomnum, 'abcdef')
    userinfo = UserInfo.newUserInfo(user)
    userinfo.screenName = 'User One'
    userinfo.realName = 'User One'
    userinfo.save()
    return user

def create_dummy_programmer():
    randomnum = randint(0,100000)
    user = User.objects.create_user('usertwo_%s'%randomnum, 'usertwo_%s@gogogo.com'%randomnum, 'abcdef')
    userinfo = UserInfo.newUserInfo(user)
    userinfo.screenName = 'User Two'
    userinfo.realName = 'User Two'
    userinfo.save()
    return user

def create_dummy_project():
    sponsor = create_dummy_sponsor()
    project = Project.newProject('Hibernate', sponsor, 'http://www.hibernate.org', 'https://hibernate.onjira.com/')
    project.save()
    return project

def create_dummy_issue():
    project = create_dummy_project()
    issue = Issue.newIssue(project, 'HHH-1051', 'Compiled native SQL queries are not cached', project.createdByUser, 'https://hibernate.onjira.com/browse/HHH-1051')
    issue.save()
    return issue

def create_dummy_offer():
    issue = create_dummy_issue()
    offer = Offer.newOffer(issue, issue.createdByUser, Decimal('10.00'), 'USD', 'comita aih', True, True, None)
    offer.save()
    return offer

def create_dummy_solution():
    issue = create_dummy_issue()
    programmer = create_dummy_programmer()
    solution = Solution.newSolution(issue, programmer, False)
    solution.save()
    return solution

def create_dummy_payment():
    offer = create_dummy_offer()
    payment = Payment.newPayment(offer)
    payment.setPaykey('PK_ABCDEFG')
    payment.fee = Decimal('0.30')
    payment.total = Decimal('10.00')
    payment.confirm_key = 'abcd1234'
    payment.save()
    solution = create_dummy_solution()
    part = PaymentPart.newPart(payment, solution, Decimal('10.00'), Decimal('9.70'))
    part.save()
    return payment