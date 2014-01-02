# -*- coding: UTF-8 -*-
import json
from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
import hashlib, time, random
from core.utils.frespo_utils import get_or_none, strip_protocol, as_time_string
from social_auth.models import UserSocialAuth
from django.utils.http import urlquote
from django.template.defaultfilters import slugify
from django.dispatch import receiver
from emailmgr.signals import user_activated_email
from decimal import Decimal
from core.utils.frespo_utils import twoplaces
from bitcoin_frespo.models import *
from frespo_currencies import currency_service
from django.conf import settings
from django.core.urlresolvers import reverse

_CURRENCY_SYMBOLS = {'USD': 'US$', 'BRL': 'R$', 'BTC': 'BTC'}

class UserInfo(models.Model): 
    user = models.ForeignKey(User)
    paypalEmail = models.EmailField(max_length=256)
    screenName = models.CharField(max_length=64)
    realName = models.CharField(max_length=256)
    website = models.CharField(max_length=128, null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    receiveAllEmail = models.BooleanField()
    brazilianPaypal = models.BooleanField()
    is_primary_email_verified = models.BooleanField()
    is_paypal_email_verified = models.BooleanField()
    hide_from_userlist = models.BooleanField()
    preferred_language_code = models.CharField(max_length=10, null=True, blank=True)
    bitcoin_receive_address = models.CharField(max_length=128, blank=True)
    paypal_verified = models.BooleanField()
    receiveEmail_issue_comments = models.BooleanField()
    receiveEmail_issue_work = models.BooleanField()
    receiveEmail_issue_offer = models.BooleanField()
    receiveEmail_issue_payment = models.BooleanField()
    receiveEmail_announcements = models.BooleanField()

    @classmethod
    def newUserInfo(cls, user):
        userinfo = cls()
        userinfo.user = user
        userinfo.paypalEmail = user.email
        userinfo.is_primary_email_verified = True
        userinfo.is_paypal_email_verified = True
        userinfo.screenName = user.username
        userinfo.website = ''
        userinfo.about = ''
        userinfo.realName = user.first_name+' '+user.last_name
        userinfo.receiveEmail_issue_comments = True
        userinfo.receiveEmail_issue_work = True
        userinfo.receiveEmail_issue_offer = True
        userinfo.receiveEmail_issue_payment = True
        userinfo.receiveEmail_announcements = True
        userinfo.brazilianPaypal = False
        userinfo.hide_from_userlist = False
        userinfo.paypal_verified = False
        return userinfo

    def is_differentPaypalEmail(self):
        is_different = self.paypalEmail and self.paypalEmail != self.user.email
        return is_different

    def get_website_url(self):
        if(self.website.startswith("http://") or self.website.startswith("https://")):
            return self.website
        else:
            return "http://"+self.website

    def get_website_short(self):
        if self.website and len(self.website) > 40:
            return self.website[0:40]+'...'
        return self.website

    def is_complete(self):
        return self.screenName and self.realName and self.user.email


def gravatar_url_small(self):
    gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(self.email.lower()).hexdigest() + "?"
    # return gravatar_url + urllib.urlencode({'d':settings.SITE_HOME+"/static/img/user_23.png", 's':"23"})
    return gravatar_url + "d=identicon&s=23"


def gravatar_url_medium(self):
    gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(self.email.lower()).hexdigest() + "?"
    # return gravatar_url + urllib.urlencode({'d':settings.SITE_HOME+"/static/img/user_48.png", 's':"48"})
    return gravatar_url + "d=identicon&s=50"


def gravatar_url_big(self):
    gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(self.email.lower()).hexdigest() + "?"
    # return gravatar_url + urllib.urlencode({'d':settings.SITE_HOME+"/static/img/user_128.png", 's':"128"})
    return gravatar_url + "d=identicon&s=128"


def getUserInfo(self):
    return get_or_none(UserInfo, user=self)


def getSocialAuths(self):
    return UserSocialAuth.objects.filter(user=self)


def github_username(self):
    for social_auth in self.getSocialAuths():
        if social_auth.provider == 'github' and social_auth.extra_data.has_key('social_username'):
            return social_auth.extra_data['social_username']
    return None


def getOffers(self):
    return Offer.objects.filter(sponsor=self).order_by('status','-price')


def getSolutions(self):
    return Solution.objects.filter(programmer=self).order_by('-creationDate')


def getKickstartingIssues(self):
    return Issue.objects.filter(createdByUser=self, is_public_suggestion=True).order_by('-creationDate')


def getWatchedIssues(self):
    return Issue.objects.filter(id__in=Watch.objects.filter(entity='ISSUE', user=self).values('objid'))


@receiver(user_activated_email)
def set_email_verified(sender, **kwargs):
    email = kwargs.get('email_address')
    userinfo = email.user.getUserInfo()
    if email.is_primary:
        userinfo.is_primary_email_verified = True
    else:
        userinfo.is_paypal_email_verified = True
    userinfo.save()


def get_view_link(self):
    kwargs = {'user_id': self.id}
    if(self.getUserInfo() and self.getUserInfo().screenName):
        kwargs['user_slug'] = urlquote(slugify(self.getUserInfo().screenName))
    return reverse('core.views.user_views.viewUser', kwargs=kwargs)


def is_registration_complete(self):
    return self.getUserInfo() and self.getUserInfo().is_complete()


def getStats(self):
    stats = {'sponsoredOpenCount' : 0,
        'sponsoredOpenPrice' : Decimal(0),
        'sponsoredRevokedCount' : 0,
        'sponsoredRevokedPrice' : Decimal(0),
        'sponsoredPaidCount' : 0,
        'sponsoredPaidPrice' : Decimal(0),
        'workingInProgressCount' : 0,
        'workingAbortedCount' : 0,
        'workingDoneCount' : 0}
    for offer in self.getOffers():
        if(offer.status == Offer.OPEN):
            stats['sponsoredOpenCount'] += 1
            stats['sponsoredOpenPrice'] += offer.price
        elif(offer.status == Offer.REVOKED):
            stats['sponsoredRevokedCount'] += 1
            stats['sponsoredRevokedPrice'] += offer.price
        elif(offer.status == Offer.PAID):
            stats['sponsoredPaidCount'] += 1
            stats['sponsoredPaidPrice'] += offer.price
    for solution in self.getSolutions():
        if(solution.status == Solution.IN_PROGRESS):
            stats['workingInProgressCount'] += 1
        elif(solution.status == Solution.ABORTED):
            stats['workingAbortedCount'] += 1
        elif(solution.status == Solution.DONE):
            stats['workingDoneCount'] += 1
    return stats


_socialImages_small = {'google' : '/static/img/google_small.png',
    'yahoo':'/static/img/yahoo_small.png',
    'facebook':'/static/img/facebook_small.png',
    'twitter':'/static/img/twitter_small.png',
    'github' : '/static/img/github_small.gif',
    'bitbucket' : '/static/img/bitbucket_small.png',
#    'myopenid' : '/static/img/myopenid.png'
}


_socialImages = {'google' : '/static/img/google.gif',
    'yahoo':'/static/img/yahoo.gif',
    'facebook':'/static/img/facebook.gif',
    'twitter':'/static/img/twitter.png',
    'github' : '/static/img/github.png',
    'bitbucket' : '/static/img/bitbucket.jpg',
#    'myopenid' : '/static/img/myopenid.png'
}


def getUnconnectedSocialAccounts(self):
    all_social_auths = set(_socialImages.keys())
    user_social_auths = set(auth.provider for auth in self.getSocialAuths())
    unconnected = all_social_auths - user_social_auths
    return [{'provider': p, 'icon': _socialImages.get(p)} for p in unconnected]


User.gravatar_url_small = gravatar_url_small
User.gravatar_url_medium = gravatar_url_medium
User.gravatar_url_big = gravatar_url_big
User.getUserInfo = getUserInfo
User.getSocialAuths = getSocialAuths
User.getUnconnectedSocialAccounts = getUnconnectedSocialAccounts
User.github_username = github_username
User.getOffers = getOffers
User.getSolutions = getSolutions
User.getKickstartingIssues = getKickstartingIssues
User.getWatchedIssues = getWatchedIssues
User.getStats = getStats
User.is_registration_complete = is_registration_complete
User.get_view_link = get_view_link


def getSocialIcon(self):
    return _socialImages.get(self.provider)


def getSocialIcon_small(self):
    return _socialImages_small.get(self.provider)


def getSocialProfileLink(self):
    if(self.provider == 'facebook'):
        return 'http://www.facebook.com/'+self.uid
    elif(self.provider == 'github' and self.extra_data.has_key('social_username')):
        return 'http://github.com/'+self.extra_data['social_username']
    elif(self.provider == 'twitter' and self.extra_data.has_key('social_username')):
        return 'http://twitter.com/'+self.extra_data['social_username']
    else: 
        return None


UserSocialAuth.getSocialIcon = getSocialIcon
UserSocialAuth.getSocialIcon_small = getSocialIcon_small
UserSocialAuth.getSocialProfileLink = getSocialProfileLink


def upload_to(name):
    def f(project, filename):
        extension = filename.split('.')[-1]
        timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
        return '%s_%s_%s.%s' % (name, project.id, timestamp, extension)
    return f


# Tudo que estah marcado como "@Auditable" eh um lembrete que pode ter algum atributo que eh alterado pelo
# usuário depois que a entidade eh criada.
# Essas alteracoes precisam ser gravadas em tabelas auxiliares (que a gente cria depois)

# Usuarios podem criar cadastro de projetos open-source existentes, como o Maven, o Jenkins, etc.
# Quando a gente lançar o sistema já vamos colocar vários aí.
# Precisa ter algum tipo de validação que minimize o cadastro de projetos duplicados.
#@Auditable
class Project(models.Model): 
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    createdByUser = models.ForeignKey(User)
    creationDate = models.DateTimeField()
    homeURL = models.URLField(null=True, blank=True)
    trackerURL = models.URLField(null=True, blank=True)
    image3x1 = models.ImageField(null=True, upload_to=upload_to('project_images/image3x1'))

    @classmethod
    def newProject(cls, name, createdByUser, homeURL, trackerURL):
        project = cls()
        project.name = name
        project.creationDate = timezone.now()
        project.createdByUser = createdByUser
        project.homeURL = homeURL
        project.trackerURL = trackerURL
        return project

    def get_view_link(self):
        return '/core/issue/?s=&project_id=%s&project_name=%s' % (self.id,urlquote(self.name),)

    def get_image3x1(self):
        if not self.image3x1:
            if 'github' in self.trackerURL:
                return '/static/img2/github_logo.jpg'
            else:
                return '/static/img2/default_project_logo.png'
        return '%s/%s' % (settings.MEDIA_ROOT_URL, self.image3x1)

    def get_tags(self):
        return Tag.objects.filter(objtype="Project", objid=self.id)

    def to_dict_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'homeURL': self.homeURL,
            'trackerURL': self.trackerURL,
            'image3x1': self.image3x1.url if self.image3x1 else None,
        }

    def to_json(self):
        return json.dumps(self.to_dict_json())

    def __unicode__(self):
        return self.name
    

# A tag on something
class Tag(models.Model):
    name = models.CharField(max_length=200)
    objtype = models.CharField(max_length=200)
    objid = models.IntegerField()


# Uma issue de um projeto open source.
# Isso aqui vai ser criado junto com a primeira "Offer" associada
#@Auditable
class Issue(models.Model):
    project = models.ForeignKey(Project, null=True, blank=True)
    key = models.CharField(max_length=30, null=True, blank=True)
    title = models.CharField(max_length=400)
    description = models.TextField(null=True, blank=True)
    createdByUser = models.ForeignKey(User)
    creationDate = models.DateTimeField()
    updatedDate = models.DateTimeField(null=True, blank=True)
    trackerURL = models.URLField(null=True, blank=True)
    trackerURL_noprotocol = models.URLField(null=True, blank=True)
    is_feedback = models.BooleanField()
    is_public_suggestion = models.BooleanField()
    status = models.CharField(max_length=40)

    @classmethod
    def newIssue(cls, project, key, title, description, createdByUser, trackerURL):
        issue = cls()
        issue.project = project
        issue.key = key
        issue.description = description
        issue.title = title
        issue.creationDate = timezone.now()
        issue.updatedDate = issue.creationDate
        issue.createdByUser = createdByUser
        issue.trackerURL = trackerURL
        issue.trackerURL_noprotocol = strip_protocol(trackerURL)
        issue.is_feedback = False
        issue.status = 'open'
        return issue

    @classmethod
    def newIssueOrphan(cls, title, description, createdByUser):
        issue = cls()
        issue.title = title
        issue.key = ''
        issue.description = description
        issue.creationDate = timezone.now()
        issue.updatedDate = issue.creationDate
        issue.createdByUser = createdByUser
        issue.is_feedback = False
        issue.status = 'open'
        return issue

    @classmethod
    def newIssueFeedback(cls, title, description, createdByUser):
        issue = cls()
        issue.title = title
        issue.key = ''
        issue.description = description
        issue.creationDate = timezone.now()
        issue.updatedDate = issue.creationDate
        issue.createdByUser = createdByUser
        issue.is_feedback = True
        issue.status = 'open'
        return issue

    def changeIssue(self, issuedict):
        if issuedict.get('description'):
            self.description = issuedict.get('description')
        if issuedict.get('title'):
            self.title = issuedict.get('title')
        self.touch()

    def to_dict_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'link': self.get_view_link(),
        }

    def to_json(self):
        return json.dumps(self.to_dict_json())

    def getTotalOffersPriceUSD(self):
        return self.getTotalOffersPrice_by_currency('USD')

    def getTotalOffersPriceBTC(self):
        return self.getTotalOffersPrice_by_currency('BTC')

    def getTotalOffersPrice_by_currency(self, currency):
        offers = Offer.objects.filter(issue=self, status=Offer.OPEN,currency=currency)
        s = Decimal(0)
        for offer in offers:
            if not offer.is_expired():
                s = s + offer.price
        return twoplaces(s)

    def getTotalPaidPriceUSD(self):
        return self.getTotalPaidPrice_by_currency('USD')

    def getTotalPaidPriceBTC(self):
        return self.getTotalPaidPrice_by_currency('BTC')

    def getTotalPaidPrice_by_currency(self, currency):
        offers = Offer.objects.filter(issue=self, status=Offer.PAID, currency=currency)
        s = Decimal(0)
        for offer in offers:
            s = s + offer.price
        return twoplaces(s)

    def touch(self):
        self.updatedDate = timezone.now()
        self.save()

    def countSolutionsDone(self):
        return Solution.objects.filter(issue=self, status=Solution.DONE).count()

    def countSolutionsInProgress(self):
        return Solution.objects.filter(issue=self, status=Solution.IN_PROGRESS).count()

    def getOffers(self):
        return Offer.objects.filter(issue=self).order_by('status','-price')

    def getSolutions(self):
        return Solution.objects.filter(issue=self).order_by('-creationDate')

    def getSolutionsDone(self):
        return Solution.objects.filter(issue=self, status=Solution.DONE).order_by('creationDate')

    def getSolutionsAcceptingPayments(self):
        return Solution.objects.filter(issue=self, accepting_payments=True)

    def getComments(self):
        return IssueComment.objects.filter(issue=self).order_by('creationDate')

    def get_view_link(self):
        return '/core/issue/%s'%self.id+'/'+urlquote(slugify(self.title))

    def get_card_image(self):
        if self.project:
            return self.project.get_image3x1()
        else:
            return ''

    def update_redundant_fields(self):
        self.status = self.get_status()
        self.touch()
        self.save()

    def get_status(self):
        working = False
        for solution in self.getSolutions():
            if solution.status == Solution.DONE:
                return 'done'
            elif solution.status == Solution.IN_PROGRESS:
                working = True
        return 'working' if working else 'open'

    def __unicode__(self):
        s = ''
        if(self.project):
            s += '('+self.project.name+') '
        if (self.key):
            s += self.key+': '
        s += self.title
        return s


# A record that indicates that a user is watching an issue
class Watch(models.Model):
    issue = models.ForeignKey(Issue, null=True)
    objid = models.IntegerField()
    user = models.ForeignKey(User)
    reason = models.CharField(max_length=30, null=False, blank=False)
    entity = models.CharField(max_length=60)

    CREATED = "CREATED"
    COMMENTED = "COMMENTED"
    SPONSORED = "SPONSORED"
    WATCHED = "WATCHED"
    STARTED_WORKING = "STARTED_WORKING"

    @classmethod
    def newWatch(cls, user, entity, objid, reason):
        watch = cls()
        watch.objid = objid
        watch.entity = entity
        watch.user = user
        watch.reason = reason
        return watch

# Um comentario que pode ser adicionado numa issue por qualquer pessoa
#@Auditable
class IssueComment(models.Model):
    issue = models.ForeignKey(Issue)
    author = models.ForeignKey(User)
    creationDate = models.DateTimeField()
    content = models.TextField()

    def to_json(self):
        return json.dumps({
            'content': self.content
        })

    @classmethod
    def newComment(cls, issue, author, content):
        comment = cls()
        comment.issue = issue
        comment.author = author
        comment.creationDate = timezone.now()
        comment.content = content
        return comment

    def changeContent(self, content):
        event = IssueCommentHistEvent.newChangeEvent(self, IssueCommentHistEvent.EDIT)
        event.save()
        self.content = content
        self.save()

    def was_edited(self):
        return IssueCommentHistEvent.objects.filter(comment__id = self.id).count() > 0

class IssueCommentHistEvent(models.Model):
    comment = models.ForeignKey(IssueComment)
    eventDate = models.DateTimeField()
    content = models.TextField()
    event = models.CharField(max_length=30)

    EDIT = "EDIT"

    @classmethod
    def newChangeEvent(cls, comment, event):
        evt = cls()
        evt.comment = comment
        evt.eventDate = timezone.now()
        evt.content = comment.content
        evt.event = event
        return evt

# Uma oferta de dinheiro feita por um sponsor em potencial
#@Auditable
class Offer(models.Model):
    issue = models.ForeignKey(Issue)
    sponsor = models.ForeignKey(User)
    creationDate = models.DateTimeField()
    lastChangeDate = models.DateTimeField()
    price = models.DecimalField(max_digits=9, decimal_places=2) # Ateh 9999999.99 dolares
    currency = models.CharField(max_length=10)
    acceptanceCriteria = models.TextField(null=True, blank=True)
    expirationDate = models.DateField(null=True, blank=True)
    no_forking = models.BooleanField(default=True)
    require_release = models.BooleanField(default=True)
    status = models.CharField(max_length=30)
    
    OPEN = "OPEN"
    REVOKED = "REVOKED"
    PAID = "PAID"

    def to_dict_json(self):
        return {
            'id': self.id,
            'price': float(str(self.price)),
            'currency': self.currency,
            'acceptanceCriteria': self.acceptanceCriteria,
            'no_forking': self.no_forking,
            'require_release': self.require_release,
            'status': self.status,
        }

    def to_json(self):
        return json.dumps(self.to_dict_json())

    @classmethod
    def newOffer(cls, issue, sponsor, price, currency, acceptanceCriteria, no_forking, require_release, expiration_days):
        offer = cls()
        offer.issue = issue
        offer.sponsor = sponsor
        offer.creationDate = timezone.now()
        offer.lastChangeDate = offer.creationDate
        offer.price = Decimal(price)
        offer.currency = currency
        offer.acceptanceCriteria = acceptanceCriteria
        offer.no_forking = no_forking
        offer.require_release = require_release
        offer.set_expiration_days(expiration_days)
        offer.status = Offer.OPEN
        return offer

    def get_currency_symbol(self):
        return _CURRENCY_SYMBOLS[self.currency]

    def price_2(self):
        return twoplaces(self.price)

    def set_expiration_days(self, expiration_days):
        if(expiration_days and expiration_days > 0):
            self.expirationDate = timezone.now() + timedelta(days=expiration_days)

    def clone(self):
        clone_offer = Offer.newOffer(self.issue, self.sponsor, Decimal(self.price), self.currency, self.acceptanceCriteria,
            self.no_forking, self.require_release, self.expiration_time())
        return clone_offer

    def expires(self):
        return self.expirationDate != None and self.status == Offer.OPEN

    def is_expired(self):
        return self.expires() and timezone.now().date() > self.expirationDate

    def expiration_time(self):
        if(self.expires()):
            return (self.expirationDate - timezone.now().date()).days
        else:
            return -1

    def changeOffer(self, offerdict):
        self.currency = offerdict['currency']
        self.price = Decimal(offerdict['price'])
        self.acceptanceCriteria = offerdict['acceptanceCriteria']
        self.no_forking = offerdict.has_key('no_forking')
        self.require_release = offerdict.has_key('require_release')
        if(offerdict.has_key('expires')):
            self.set_expiration_days(int(offerdict['expiration_time']))
        else:
            self.expirationDate = None
        self.status = Offer.OPEN
        self.lastChangeDate = timezone.now()
        self.save()

    def revoke(self):
        self.status = Offer.REVOKED
        self.lastChangeDate = timezone.now()
        self.save()

    def paid(self):
        self.status = Offer.PAID
        self.lastChangeDate = timezone.now()
        self.save()

    def getComments(self):
        return OfferComment.objects.filter(offer=self).order_by('creationDate')

    def get_payments(self):
        if self.status == Offer.PAID:
            return Payment.objects.filter(offer__id=self.id, status__in=[Payment.CONFIRMED_IPN, Payment.CONFIRMED_TRN])
        return []

    def get_view_link(self):
        return '/core/offer/%s'%self.id+'/'+urlquote(slugify(self.issue.title))


# Um comentario que pode ser adicionado numa offer por qualquer pessoa.
# É um fórum mais restrito do que os comentarios da issue. Pode ser util por exemplo 
# quando o programador quiser por exemplo quiser tirar satisfação com um dos sponsors que ainda 
# não pagou a offer de uma issue bem resolvida.
# Serve também pra "queimar" o filme do sponsor caloteiro pq fica associado direto com a reputação dele.
#@Auditable
class OfferComment(models.Model):
    offer = models.ForeignKey(Offer)
    author = models.ForeignKey(User)
    creationDate = models.DateTimeField()
    content = models.TextField()

    @classmethod
    def newComment(cls, offer, author, content):
        comment = cls()
        comment.offer = offer
        comment.author = author
        comment.creationDate = timezone.now()
        comment.content = content
        return comment
    
    def changeContent(self, content):
        event = OfferCommentHistEvent.newChangeEvent(self, OfferCommentHistEvent.EDIT)
        event.save()
        self.content = content
        self.save()

    def was_edited(self):
        return OfferCommentHistEvent.objects.filter(comment__id = self.id).count() > 0

class OfferCommentHistEvent(models.Model):
    comment = models.ForeignKey(OfferComment)
    eventDate = models.DateTimeField()
    content = models.TextField()
    event = models.CharField(max_length=30)

    EDIT = "EDIT"

    @classmethod
    def newChangeEvent(cls, comment, event):
        evt = cls()
        evt.comment = comment
        evt.eventDate = timezone.now()
        evt.content = comment.content
        evt.event = event
        return evt


# Registro de quando o programador declara que está trabalhando / resolveu uma issue.
# Os comentarios do programador vao como IssueComment, tipo
# "Resolvi, PODEM ME PAGAR AGORA!! Uhuuu :-)
#@Auditable
class Solution(models.Model):
    issue = models.ForeignKey(Issue)
    programmer = models.ForeignKey(User)
    creationDate = models.DateTimeField()
    lastChangeDate = models.DateTimeField()
    status = models.CharField(max_length=30) # IN_PROGRESS, DONE, ABORTED
    accepting_payments = models.BooleanField()

    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
    ABORTED = "ABORTED"

    @classmethod
    def newSolution(cls, issue, programmer, accepting_payments):
        solution = cls()
        solution.issue = issue
        solution.programmer = programmer
        solution.creationDate = timezone.now()
        solution.lastChangeDate = solution.creationDate
        solution.status = Solution.IN_PROGRESS
        solution.accepting_payments = accepting_payments
        return solution

    def abort(self):
        self.status = Solution.ABORTED
        self.lastChangeDate = timezone.now()
        self.accepting_payments = False
        self.save()

    def resolve(self):
        self.status = Solution.DONE
        self.lastChangeDate = timezone.now()
        self.accepting_payments = True
        self.save()

    def reopen(self, accepting_payments):
        self.status = Solution.IN_PROGRESS
        self.lastChangeDate = timezone.now()
        self.accepting_payments = accepting_payments
        self.save()

    def get_received_payments(self):
        return PaymentPart.objects.filter(solution__id = self.id)


# Registro da finalização bem sucedida de uma Offer.
# Note que pode haver mais de um Payment, se o sponsor iniciar um pagamento e nao finalizar
class Payment(models.Model):
    offer = models.ForeignKey(Offer)
    creationDate = models.DateTimeField()
    lastChangeDate = models.DateTimeField()
    paykey = models.CharField(max_length=128, null=True, blank=True)
    confirm_key = models.CharField(max_length=128, null=True, blank=True)
    status = models.CharField(max_length=30)
    fee = models.DecimalField(max_digits=16, decimal_places=8)
    total = models.DecimalField(max_digits=16, decimal_places=8)
    currency = models.CharField(max_length=10)
    bitcoin_receive_address = models.ForeignKey(ReceiveAddress, null=True)
    bitcoin_transaction_hash = models.CharField(max_length=128, null=True)
    total_bitcoin_received = models.DecimalField(max_digits=16, decimal_places=8, null=True)
    bitcoin_fee = models.DecimalField(max_digits=16, decimal_places=8, null=True)
    offer_currency = models.CharField(max_length=10, null=True)
    offer2payment_suggested_rate = models.DecimalField(max_digits=16, decimal_places=8, null=True)
    usd2payment_rate = models.DecimalField(max_digits=16, decimal_places=8, null=True)

    CREATED = 'CREATED'
    CANCELED = 'CANCELED'
    CONFIRMED_WEB = 'CONFIRMED_WEB'
    CONFIRMED_IPN = 'CONFIRMED_IPN'
    CONFIRMED_IPN_UNDERPAY = 'CONFIRMED_IPN_UNDERPAY'
    CONFIRMED_TRN = 'CONFIRMED_TRN'
    CONFIRMED_TRN_UNDERPAY = 'CONFIRMED_TRN_UNDERPAY'
    FORGOTTEN = 'FORGOTTEN'

    def to_dict_json(self):
        return {
            'id': self.id,
            'status': self.status,
            'fee': float(str(self.fee)) if self.fee else None,
            'total': float(str(self.total)) if self.total else None,
            'total_bitcoin_received': float(str(self.total_bitcoin_received)) if self.total_bitcoin_received else None,
            'bitcoin_fee': float(str(self.bitcoin_fee)) if self.bitcoin_fee else None,
            'offer2payment_suggested_rate': float(str(self.offer2payment_suggested_rate)) if self.offer2payment_suggested_rate else None,
            'usd2payment_rate': float(str(self.usd2payment_rate)) if self.usd2payment_rate else None,
            'currency': self.currency,
            'bitcoin_transaction_hash': self.bitcoin_transaction_hash,
            'offer_currency': self.offer_currency,
            'parts': [part.to_dict_json() for part in self.getParts()]
        }

    def to_json(self):
        return json.dumps(self.to_dict_json())

    @classmethod
    def newPayment(cls, offer, currency):
        payment = cls()
        payment.offer = offer
        payment.currency = currency
        payment.offer_currency = offer.currency
        payment.offer2payment_suggested_rate = Decimal(str(currency_service.get_rate(offer.currency, payment.currency)))
        payment.usd2payment_rate = Decimal(str(currency_service.get_rate('USD', payment.currency)))
        payment.creationDate = timezone.now()
        payment.lastChangeDate = payment.creationDate
        payment.status = Payment.CREATED
        payment.confirm_key = hashlib.md5(str(time.time()) + str(random.random())).hexdigest()
        return payment
    
    def get_currency_symbol(self):
        return _CURRENCY_SYMBOLS[self.currency]

    def total_with_fee(self):
        return self.total + self.fee + self.bitcoin_fee

    def setPaykey(self, paykey):
        self.paykey = paykey

    def getParts(self):
        return PaymentPart.objects.filter(payment=self)

    def is_confirmed(self):
        return self.status == Payment.CONFIRMED_WEB or self.status == Payment.CONFIRMED_IPN

    def touch(self):
        self.lastChangeDate = timezone.now()

    def cancel(self):
        event = PaymentHistEvent.newChangeEvent(payment=self, event=PaymentHistEvent.CANCEL)
        event.save()
        if not self.is_confirmed():
            self.status = Payment.CANCELED
            self.touch()
            self.save()
        else:
            raise BaseException('canceled confirmed payment %s' % self.id)

    def forget(self):
        event = PaymentHistEvent.newChangeEvent(payment=self, event=PaymentHistEvent.FORGET)
        event.save()
        if self.status == Payment.CREATED:
            self.status = Payment.FORGOTTEN
            self.touch()
            self.save()
        else:
            raise BaseException('forgot %s payment %s' % (self.status, self.id))

    def confirm_web(self):
        event = PaymentHistEvent.newChangeEvent(payment=self, event=PaymentHistEvent.CONFIRM_WEB)
        event.save()
        if self.status != Payment.CONFIRMED_IPN:
            self.status = Payment.CONFIRMED_WEB
            self.touch()
            self.save()

    def confirm_ipn(self):
        event = PaymentHistEvent.newChangeEvent(payment=self, event=PaymentHistEvent.CONFIRM_IPN)
        event.save()
        self.status = Payment.CONFIRMED_IPN
        self.touch()
        self.save()

    def confirm_bitcoin_ipn(self, value, transaction_hash):
        if self.status == Payment.CREATED:
            if value >= self.total_with_fee() - Decimal('0.001'):
                self.status = Payment.CONFIRMED_IPN
            else:
                self.status = Payment.CONFIRMED_IPN_UNDERPAY
            self.total_bitcoin_received = value
        self.bitcoin_transaction_hash = transaction_hash
        self.touch()
        self.save()

    def confirm_bitcoin_trn(self, value):
        self.total_bitcoin_received = Decimal(str(value))
        if self.total_bitcoin_received >= self.total_with_fee() - Decimal('0.001'):
            self.status = Payment.CONFIRMED_TRN
        else:
            self.status = Payment.CONFIRMED_TRN_UNDERPAY
        self.touch()
        self.save()


class PaymentHistEvent(models.Model):
    payment = models.ForeignKey(Payment)
    eventDate = models.DateTimeField()
    status = models.CharField(max_length=30)
    event = models.CharField(max_length=30)

    CANCEL = "CANCEL"
    CONFIRM_WEB = "CONFIRM_WEB"
    CONFIRM_IPN = "CONFIRM_IPN"
    FORGET = "FORGET"

    @classmethod
    def newChangeEvent(cls, payment, event):
        evt = cls()
        evt.payment = payment
        evt.eventDate = timezone.now()
        evt.status = payment.status
        evt.event = event
        return evt


# Parcela de um Payment paga pra um dado programador
# (Vai ter mais de um, se o sponsor decidir pagar pra mais de um programador)
class PaymentPart(models.Model):
    payment = models.ForeignKey(Payment)
    programmer = models.ForeignKey(User)
    solution = models.ForeignKey(Solution)
    paypalEmail = models.EmailField(max_length=256, null=True)
    price = models.DecimalField(max_digits=16, decimal_places=8)
    money_sent = models.ForeignKey(MoneySent, null=True)

    def to_dict_json(self):
        return {
            'id': self.id,
            'programmer_id': self.programmer.id,
            'programmer_image': self.programmer.gravatar_url_small(),
            'programmer_screenname': self.programmer.getUserInfo().screenName,
            'solution_id': self.solution.id,
            'price': float(str(self.price)) if self.price else None,
        }

    @classmethod
    def newPart(cls, payment, solution, price):
        part = cls()
        part.payment = payment
        part.solution = solution
        part.programmer = solution.programmer
        part.paypalEmail = part.programmer.getUserInfo().paypalEmail
        part.price = Decimal(price)
        return part


# A historical log event
class ActionLog(models.Model):
    action = models.CharField(max_length=128, null=False, blank=False)
    entity = models.CharField(max_length=30, null=False, blank=False)
    old_json = models.TextField(null=True)
    new_json = models.TextField(null=True)
    creationDate = models.DateTimeField(null=False)
    user = models.ForeignKey(User, null=True)
    project = models.ForeignKey(Project, null=True)
    issue = models.ForeignKey(Issue, null=True)
    offer = models.ForeignKey(Offer, null=True)
    solution = models.ForeignKey(Solution, null=True)
    payment = models.ForeignKey(Payment, null=True)
    issue_comment = models.ForeignKey(IssueComment, null=True)

    EDIT_ISSUE = 'EDIT_ISSUE'
    EDIT_PROJECT = 'EDIT_PROJECT'
    PROJECT_ADD_TAG = 'PROJECT_ADD_TAG'
    PROJECT_REMOVE_TAG = 'PROJECT_REMOVE_TAG'
    SPONSOR = 'SPONSOR'
    CHANGE_OFFER = 'CHANGE_OFFER'
    REVOKE = 'REVOKE'
    PROPOSE = 'PROPOSE'
    WORK = 'WORK'
    ABORT = 'ABORT'
    RESOLVE = 'RESOLVE'
    PAY = 'PAY'
    ADD_ISSUE_COMMENT = 'ADD_ISSUE_COMMENT'
    EDIT_ISSUE_COMMENT = 'EDIT_ISSUE_COMMENT'

    def to_dict_json(self):
        return {
            'id': self.id,
            'creationDate': str(self.creationDate),
            'when': as_time_string(self.creationDate),
            'action': self.action,
            'entity': self.entity,
            # 'creationDate': self.id,
            'user_image': self.user.gravatar_url_medium(),
            'user_screenname': self.user.getUserInfo().screenName,
            'user_id': self.user.id,
            'project_id': self.project.id if self.project else None,
            'project': self.project.to_dict_json() if self.project else None,
            'issue_id': self.issue.id if self.issue else None,
            'issue': self.issue.to_dict_json() if self.issue else None,
            'offer_id': self.offer.id if self.offer else None,
            'offer': self.offer.to_dict_json() if self.offer else None,
            'payment_id': self.payment.id if self.payment else None,
            'payment': self.payment.to_dict_json() if self.payment else None,
            'solution_id': self.solution.id if self.solution else None,
            'issue_comment_id': self.issue_comment.id if self.issue_comment else None,
            'issue_comment_content': self.issue_comment.content if self.issue_comment else None,
            'old_json': self.old_json,
            'new_json': self.new_json,
        }

    @classmethod
    def log_edit_issue(cls, issue, user, old_json):
        new_json = issue.to_json()
        ActionLog(
            creationDate=timezone.now(),
            action=ActionLog.EDIT_ISSUE,
            entity='ISSUE',
            old_json=old_json,
            new_json=new_json,
            issue=issue,
            project=issue.project,
            user=user,
        ).save()

    @classmethod
    def log_edit_project(cls, project, user, old_json):
        new_json = project.to_json()
        ActionLog(
            creationDate=timezone.now(),
            action=ActionLog.EDIT_PROJECT,
            entity='PROJECT',
            old_json=old_json,
            new_json=new_json,
            project=project,
            user=user,
        ).save()

    @classmethod
    def log_project_tag_added(cls, user, project_id, tag_name):
        ActionLog(
            creationDate=timezone.now(),
            action=ActionLog.PROJECT_ADD_TAG,
            entity='PROJECT',
            new_json=tag_name,
            project=Project(id=project_id),
            user=user,
        ).save()

    @classmethod
    def log_project_tag_removed(cls, user, project_id, tag_name):
        ActionLog(
            creationDate=timezone.now(),
            action=ActionLog.PROJECT_REMOVE_TAG,
            entity='PROJECT',
            new_json=tag_name,
            project=Project(id=project_id),
            user=user,
        ).save()

    @classmethod
    def log_sponsor(cls, offer):
        ActionLog(
            creationDate=timezone.now(),
            action=ActionLog.SPONSOR,
            entity='OFFER',
            new_json=offer.to_json(),
            project=offer.issue.project,
            issue=offer.issue,
            offer=offer,
            user=offer.sponsor,
        ).save()

    @classmethod
    def log_propose(cls, issue, user):
        ActionLog(
            creationDate=timezone.now(),
            action=ActionLog.PROPOSE,
            entity='ISSUE',
            new_json=issue.to_json(),
            project=issue.project,
            issue=issue,
            user=user,
        ).save()

    @classmethod
    def log_change_offer(cls, offer, user, old_json):
        ActionLog(
            creationDate=timezone.now(),
            action=ActionLog.CHANGE_OFFER,
            entity='OFFER',
            old_json=old_json,
            new_json=offer.to_json(),
            project=offer.issue.project,
            issue=offer.issue,
            offer=offer,
            user=user,
        ).save()

    @classmethod
    def log_revoke(cls, offer, user, issue_comment):
        ActionLog(
            creationDate=timezone.now(),
            action=ActionLog.REVOKE,
            entity='OFFER',
            new_json=offer.to_json(),
            project=offer.issue.project,
            issue=offer.issue,
            offer=offer,
            issue_comment=issue_comment,
            user=user,
        ).save()

    @classmethod
    def log_start_work(cls, solution, issue_comment):
        ActionLog(
            creationDate=timezone.now(),
            action=ActionLog.WORK,
            entity='SOLUTION',
            project=solution.issue.project,
            issue=solution.issue,
            solution=solution,
            issue_comment=issue_comment,
            user=solution.programmer,
        ).save()

    @classmethod
    def log_abort_work(cls, solution, issue_comment):
        ActionLog(
            creationDate=timezone.now(),
            action=ActionLog.ABORT,
            entity='SOLUTION',
            project=solution.issue.project,
            issue=solution.issue,
            solution=solution,
            issue_comment=issue_comment,
            user=solution.programmer,
        ).save()

    @classmethod
    def log_resolve(cls, solution, issue_comment):
        ActionLog(
            creationDate=timezone.now(),
            action=ActionLog.RESOLVE,
            entity='SOLUTION',
            project=solution.issue.project,
            issue=solution.issue,
            solution=solution,
            issue_comment=issue_comment,
            user=solution.programmer,
        ).save()

    @classmethod
    def log_add_issue_comment(cls, issue_comment):
        ActionLog(
            creationDate=timezone.now(),
            action=ActionLog.ADD_ISSUE_COMMENT,
            entity='ISSUE_COMMENT',
            project=issue_comment.issue.project,
            issue=issue_comment.issue,
            issue_comment=issue_comment,
            new_json=issue_comment.to_json(),
            user=issue_comment.author,
        ).save()

    @classmethod
    def log_edit_issue_comment(cls, issue_comment, old_json):
        ActionLog(
            creationDate=timezone.now(),
            action=ActionLog.EDIT_ISSUE_COMMENT,
            entity='ISSUE_COMMENT',
            project=issue_comment.issue.project,
            issue=issue_comment.issue,
            issue_comment=issue_comment,
            new_json=issue_comment.to_json(),
            old_json=old_json,
            user=issue_comment.author,
        ).save()

    @classmethod
    def log_pay(cls, payment):
        ActionLog(
            creationDate=timezone.now(),
            action=ActionLog.PAY,
            entity='PAYMENT',
            project=payment.offer.issue.project,
            issue=payment.offer.issue,
            payment=payment,
            new_json=payment.to_json(),
            user=payment.offer.sponsor,
        ).save()
