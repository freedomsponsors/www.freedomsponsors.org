from django.contrib.auth.models import User
from core.models import *
from django.utils import timezone
from social_auth.models import UserSocialAuth
from decimal import Decimal
from django.conf import settings


userDict1 = {'username':settings.TEST_GMAIL_ACCOUNT_1['username'], 
    'password':settings.TEST_GMAIL_ACCOUNT_1['password'], 
    'first_name':'Freedom', 'last_name':'Testing'}
userDict2 = {'username':settings.TEST_GMAIL_ACCOUNT_2['username'], 
    'password':settings.TEST_GMAIL_ACCOUNT_2['password'], 
    'first_name':'Outra', 'last_name':'Fake'}

paypal_credentials_1 = {'email':'spon1_1348457115_per@gmail.com',
    'password' : '12345678'}

def buildDefaultOfferDict14(trackerURL):
    return {
        'step1' : {
            'trackerURL' : trackerURL,
        },
        'step4' : _defaultOfferDict(),
    }

def buildDefaultOfferDict134(trackerURL, newProjectHomeURL):
    return {
        'step1' : {
            'trackerURL' : trackerURL,
        },
        'step3' : {
            'newProjectHomeURL' : newProjectHomeURL,
        },
        'step4' : _defaultOfferDict(),
    }
def buildDefaultOfferDict1234(trackerURL='', key='', title='', newProjectName='', newProjectHomeURL='', newProjectTrackerURL=''):
    result = {
        'step1' : {
            'trackerURL' : trackerURL,
        },
        'step2' : {
            'title' : title,
        },
        'step3' : {
            'createProject' : True,
            'newProjectName' : newProjectName,
            'newProjectHomeURL' : newProjectHomeURL,
            'newProjectTrackerURL' : newProjectTrackerURL,
        },
        'step4' : _defaultOfferDict(),
    }
    if(key):
        result['step2']['key'] = key
    return result

def buildOfferDictAvulsa():
    return {
        'step1' : {
            'noProject' : True,
        },
        'step2' : {
            'title' : 'Build me a teleporting machine',
            'description' : 'must take me anywhere, except dangerous places',
        },
        'step4' : {
            'price' : '10.00',
            'acceptanceCriteria' : 'Resolve aih',
        }
    }

def _defaultOfferDict():
    return {
        'price' : '10.00',
        'acceptanceCriteria' : 'Resolve aih',
        'no_forking' : True,
        'require_release' : True,
    }

issueDictHHH1051 = {'trackerURL':'https://hibernate.onjira.com/browse/HHH-1051', 'key':'HHH-1051', 
    'title':'Compiled native SQL queries are not cached', 
    'project_name':'Hibernate'}

def loadUsersGoogle():
    users = []
    users.append(loadUser(buildUserGoogle(userDict1)))
    users.append(loadUser(buildUserGoogle(userDict2)))
    return users

def loadUsersPlain():
    users = []
    users.append(loadUser(buildUserPlain(userDict1)))
    users.append(loadUser(buildUserPlain(userDict2)))
    return users

def buildOfferForHHH1052(createdByUser):
    hibernate = Project.objects.filter(name='Hibernate')[0]
    issue = Issue.newIssue(project=hibernate, 
        key='HHH-1052', 
        title='Allow CalendarType.set to accept Date objects', 
        createdByUser=createdByUser, 
        trackerURL='https://hibernate.onjira.com/browse/HHH-1052')
    offer = Offer.newOffer(issue=issue, 
        sponsor=createdByUser, 
        price=Decimal('10.00'), 
        acceptanceCriteria='Resolve aih', 
        no_forking=True, 
        require_release=True, 
        expiration_days=-1)
    return offer

def buildSolutionDoneFor(issue, programmer, accepting_payments):
    solution = Solution.newSolution(issue, programmer, accepting_payments)
    solution.status = Solution.DONE
    return solution

def buildUserGoogle(userdict):
    adminUser = User()
    adminUser.username = userdict['first_name']+userdict['last_name']
    adminUser.first_name = userdict['first_name']
    adminUser.last_name = userdict['last_name']
    adminUser.email = userdict['username']+'@gmail.com'
    adminUser.password = "!"
    adminUser.date_joined = timezone.now()
    userInfo = _defaultUserInfo(adminUser)
    google_auth = _googleAuth(adminUser)
    user = _Thing()
    user.adminUser = adminUser
    user.userInfo = userInfo
    user.social_auths = [google_auth]
    return user

def buildUserPlain(userdict):
    adminUser = User()
    adminUser.username = userdict['username']
    adminUser.first_name = userdict['first_name']
    adminUser.last_name = userdict['last_name']
    adminUser.email = userdict['username']+'@gmail.com'
    adminUser.set_password(userdict['password'])
    adminUser.date_joined = timezone.now()
    userInfo = _defaultUserInfo(adminUser)
    user = _Thing()
    user.adminUser = adminUser
    user.userInfo = userInfo
    user.social_auths = []
    return user

class _Thing:
    def __init__(self):
        pass
    
def loadUser(user):
    user.adminUser.save()
    user.userInfo.user = user.adminUser
    user.userInfo.save();
    for social_auth in user.social_auths:
        social_auth.user = user.adminUser
        social_auth.save()
    return user
    
def loadOffer(offer):
    offer.issue.project.save()
    offer.issue.project = offer.issue.project
    offer.issue.save()
    offer.issue = offer.issue
    offer.save()

def loadSolution(solution):
    solution.save()

def _defaultUserInfo(user):
    userInfo = UserInfo()
    userInfo.user = user
    userInfo.paypalEmail = user.email
    userInfo.screenName = user.username
    userInfo.realName = user.first_name + ' ' + user.last_name
    userInfo.website = ''
    userInfo.about = ''
    userInfo.receiveAllEmail = True
    userInfo.brazilianPaypal = False
    return userInfo
    
def _googleAuth(user):
    google_auth = UserSocialAuth()
    google_auth.user = user
    google_auth.provider = 'google'
    google_auth.uid = user.email
    google_auth.extra_data = '{}'
    return google_auth
    

    