# -*- coding: UTF-8 -*-
from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
import urllib, hashlib, time, random
from core.utils.frespo_utils import get_or_none, socialImages, socialImages_small
from social_auth.models import UserSocialAuth
from django.utils.http import urlquote
from django.template.defaultfilters import slugify
from decimal import Decimal
from aggregate_if import Sum


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
        userinfo.receiveAllEmail = True
        userinfo.brazilianPaypal = False
        userinfo.hide_from_userlist = False
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
    # return gravatar_url + urllib.urlencode({'d':"http://dl.dropbox.com/u/2683925/glyphicons_003_user.png", 's':"23"})
    return gravatar_url + urllib.urlencode({'d':settings.SITE_HOME+"/static/img/user_23.png", 's':"23"})

def gravatar_url_medium(self):
    gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(self.email.lower()).hexdigest() + "?"
    return gravatar_url + urllib.urlencode({'d':settings.SITE_HOME+"/static/img/user_48.png", 's':"48"})

def gravatar_url_big(self):
    gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(self.email.lower()).hexdigest() + "?"
    return gravatar_url + urllib.urlencode({'d':settings.SITE_HOME+"/static/img/user_128.png", 's':"128"})

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

def set_email_verified(self, is_primary):
    userinfo = self.getUserInfo()
    if is_primary:
        userinfo.is_primary_email_verified = True
    else:
        userinfo.is_paypal_email_verified = True
    userinfo.save()

def get_view_link(self):
    res = '/core/user/%s'%self.id
    if(self.getUserInfo() and self.getUserInfo().screenName):
        res += '/'+urlquote(slugify(self.getUserInfo().screenName))
    return res

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

User.gravatar_url_small = gravatar_url_small
User.gravatar_url_medium = gravatar_url_medium
User.gravatar_url_big = gravatar_url_big
User.getUserInfo = getUserInfo
User.getSocialAuths = getSocialAuths
User.github_username = github_username
User.getOffers = getOffers
User.getSolutions = getSolutions
User.getKickstartingIssues = getKickstartingIssues
User.getStats = getStats
User.is_registration_complete = is_registration_complete
User.get_view_link = get_view_link
User.set_email_verified = set_email_verified

def getSocialIcon(self):
    if(socialImages.has_key(self.provider)):
        return socialImages[self.provider]
    else:
        return None

def getSocialIcon_small(self):
    if(socialImages_small.has_key(self.provider)):
        return socialImages_small[self.provider]
    else:
        return None

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


# Tudo que estah marcado como "@Auditable" eh um lembrete que pode ter algum atributo que eh alterado pelo
# usuário depois que a entidade eh criada.
# Essas alteracoes precisam ser gravadas em tabelas auxiliares (que a gente cria depois)

# Usuarios podem criar cadastro de projetos open-source existentes, como o Maven, o Jenkins, etc.
# Quando a gente lançar o sistema já vamos colocar vários aí.
# Precisa ter algum tipo de validação que minimize o cadastro de projetos duplicados.
#@Auditable
class Project(models.Model): 
    name = models.CharField(max_length=200)
    createdByUser = models.ForeignKey(User)
    creationDate = models.DateTimeField()
    homeURL = models.URLField(null=True, blank=True)
    trackerURL = models.URLField(null=True, blank=True)
    
    @classmethod
    def newProject(cls, name, createdByUser, homeURL, trackerURL):
        project = cls()
        project.name = name
        project.creationDate = timezone.now()
        project.createdByUser = createdByUser
        project.homeURL = homeURL
        project.trackerURL = trackerURL
        return project

    def __unicode__(self):
        return self.name
    
##########
# ISSUES #
##########

class IssueManager(models.Manager):
    '''
    Custom Manager to differentiate sponsoring issues from kickstarting issues.
    '''
    def __init__(self, is_public_suggestion):
        self.is_kickstarting = is_public_suggestion
        super(IssueManager, self).__init__()

    @property
    def is_sponsoring(self):
        return not self.is_kickstarting

    def get_query_set(self):
        '''
        Always filter sponsoring OR kickstarting.
        '''
        qs = super(IssueManager, self).get_query_set()
        qs = qs.filter(Q(is_feedback=False) | Q(offer__isnull=False)).distinct()
        qs = qs.filter(is_public_suggestion=self.is_kickstarting)
        return qs

    def recently_updated(self):
        '''
        Returns issues recently updated.
        For sponsoring, also aggregate the sum of paid and open offers.
        '''
        qs = self.select_related('project__name').order_by('-updatedDate')
        if self.is_sponsoring:
            qs = qs.annotate(
                paid_amount=Sum('offer__price', only=Q(offer__status=Offer.PAID)),
                open_amount=Sum('offer__price', only=Q(offer__status=Offer.OPEN)))
        return qs


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
    is_feedback = models.BooleanField()
    is_public_suggestion = models.BooleanField()

    objects = models.Manager()
    sponsoring = IssueManager(is_public_suggestion=False)
    kickstarting = IssueManager(is_public_suggestion=True)

    @classmethod
    def newIssue(cls, project, key, title, createdByUser, trackerURL):
        issue = cls()
        issue.project = project
        issue.key = key
        issue.description = ''
        issue.title = title
        issue.creationDate = timezone.now()
        issue.updatedDate = issue.creationDate
        issue.createdByUser = createdByUser
        issue.trackerURL = trackerURL
        issue.is_feedback = False
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
        return issue

    def getTotalOffersPrice(self):
        offers = Offer.objects.filter(issue=self,status=Offer.OPEN)
        s = Decimal(0)
        for offer in offers:
            if (not offer.is_expired()):
                s = s + offer.price
        return s

    def touch(self):
        self.updatedDate = timezone.now()
        self.save()

    def getTotalPaidPrice(self):
        offers = Offer.objects.filter(issue=self,status=Offer.PAID)
        s = Decimal(0)
        for offer in offers:
            s = s + offer.price
        return s

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

    def __unicode__(self):
        s = ''
        if(self.project):
            s += '('+self.project.name+') '
        if (self.key):
            s += self.key+': '
        s += self.title
        return s

# A record that indicates that a user is watching an issue
class IssueWatch(models.Model):
    issue = models.ForeignKey(Issue)
    user = models.ForeignKey(User)
    reason = models.CharField(max_length=30, null=False, blank=False)

    CREATED = "CREATED"
    COMMENTED = "COMMENTED"
    SPONSORED = "SPONSORED"
    WATCHED = "WATCHED"
    STARTED_WORKING = "STARTED_WORKING"

    @classmethod
    def newIssueWatch(cls, issue, user, reason):
        watch = cls()
        watch.issue = issue
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
    acceptanceCriteria = models.TextField(null=True, blank=True)
    expirationDate = models.DateField(null=True, blank=True)
    no_forking = models.BooleanField(default=True)
    require_release = models.BooleanField(default=True)
    status = models.CharField(max_length=30)
    
    OPEN = "OPEN"
    REVOKED = "REVOKED"
    PAID = "PAID"

    @classmethod
    def newOffer(cls, issue, sponsor, price, acceptanceCriteria, no_forking, require_release, expiration_days):
        offer = cls()
        offer.issue = issue
        offer.sponsor = sponsor
        offer.creationDate = timezone.now()
        offer.lastChangeDate = offer.creationDate
        offer.price = Decimal(price)
        offer.acceptanceCriteria = acceptanceCriteria
        offer.no_forking = no_forking
        offer.require_release = require_release
        offer.set_expiration_days(expiration_days)
        offer.status = Offer.OPEN
        return offer

    def set_expiration_days(self, expiration_days):
        if(expiration_days and expiration_days > 0):
            self.expirationDate = timezone.now() + timedelta(days=expiration_days)

    def clone(self):
        clone_offer = Offer.newOffer(self.issue, self.sponsor, Decimal(self.price), self.acceptanceCriteria,
            self.no_forking, self.require_release, self.expiration_time())
        return clone_offer


    def expires(self):
        return self.expirationDate != None

    def is_expired(self):
        return self.expires() and timezone.now().date() > self.expirationDate

    def expiration_time(self):
        if(self.expires()):
            return (self.expirationDate - timezone.now().date()).days
        else:
            return -1

    def changeOffer(self, offerdict):
        event = OfferHistEvent.newChangeEvent(offer=self, event=OfferHistEvent.EDIT)
        event.save()
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
        event = OfferHistEvent.newChangeEvent(offer=self, event=OfferHistEvent.REVOKE)
        event.save()
        self.status = Offer.REVOKED
        self.lastChangeDate = timezone.now()
        self.save()

    def paid(self):
        event = OfferHistEvent.newChangeEvent(offer=self, event=OfferHistEvent.PAY)
        event.save()
        self.status = Offer.PAID
        self.lastChangeDate = timezone.now()
        self.save()

    def getComments(self):
        return OfferComment.objects.filter(offer=self).order_by('creationDate')

    def get_payment(self):
        if self.status == Offer.PAID:
            return get_or_none(Payment, offer__id = self.id, status = Payment.CONFIRMED_IPN)
        return None

    def get_view_link(self):
        return '/core/offer/%s'%self.id+'/'+urlquote(slugify(self.issue.title))

# A record that indicates that a user is watching an offer
class OfferWatch(models.Model):
    offer = models.ForeignKey(Offer)
    user = models.ForeignKey(User)
    reason = models.CharField(max_length=30, null=False, blank=False)

    COMMENTED = "COMMENTED"
    WATCHED = "WATCHED"

    @classmethod
    def newOfferWatch(cls, offer, user, reason):
        watch = cls()
        watch.offer = offer
        watch.user = user
        watch.reason = reason
        return watch

class OfferHistEvent(models.Model):
    offer = models.ForeignKey(Offer)
    eventDate = models.DateTimeField()
    price = models.DecimalField(max_digits=9, decimal_places=2) # Ateh 9999999.99 dolares
    acceptanceCriteria = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=30)
    expirationDate = models.DateField(null=True, blank=True)
    no_forking = models.BooleanField(default=True)
    require_release = models.BooleanField(default=True)
    event = models.CharField(max_length=30)

    EDIT = "EDIT"
    REVOKE = "REVOKE"
    PAY = "PAY"

    @classmethod
    def newChangeEvent(cls, offer, event):
        evt = cls()
        evt.offer = offer
        evt.eventDate = timezone.now()
        evt.price = Decimal(offer.price)
        evt.acceptanceCriteria = offer.acceptanceCriteria
        evt.expirationDate = offer.expirationDate
        evt.no_forking = offer.no_forking
        evt.require_release = offer.require_release
        evt.status = offer.status
        evt.event = event
        return evt

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
        event = SolutionHistEvent.newChangeEvent(solution=self, event=SolutionHistEvent.ABORT)
        event.save()
        self.status = Solution.ABORTED
        self.lastChangeDate = timezone.now()
        self.accepting_payments = False
        self.save()

    def resolve(self):
        event = SolutionHistEvent.newChangeEvent(solution=self, event=SolutionHistEvent.RESOLVE)
        event.save()
        self.status = Solution.DONE
        self.lastChangeDate = timezone.now()
        self.accepting_payments = True
        self.save()

    def reopen(self, accepting_payments):
        event = SolutionHistEvent.newChangeEvent(solution=self, event=SolutionHistEvent.REOPEN)
        event.save()
        self.status = Solution.IN_PROGRESS
        self.lastChangeDate = timezone.now()
        self.accepting_payments = accepting_payments
        self.save()

    def get_received_payments(self):
        return PaymentPart.objects.filter(solution__id = self.id)

class SolutionHistEvent(models.Model):
    solution = models.ForeignKey(Solution)
    eventDate = models.DateTimeField()
    status = models.CharField(max_length=30)
    event = models.CharField(max_length=30)

    RESOLVE = "RESOLVE"
    ABORT = "ABORT"
    REOPEN = "REOPEN"

    @classmethod
    def newChangeEvent(cls, solution, event):
        evt = cls()
        evt.solution = solution
        evt.eventDate = timezone.now()
        evt.status = solution.status
        evt.event = event
        return evt

# Registro da finalização bem sucedida de uma Offer.
# Note que pode haver mais de um Payment, se o sponsor iniciar um pagamento e nao finalizar
class Payment(models.Model):
    offer = models.ForeignKey(Offer)
    creationDate = models.DateTimeField()
    lastChangeDate = models.DateTimeField()
    paykey = models.CharField(max_length=128, null=True, blank=True)
    confirm_key = models.CharField(max_length=128, null=True, blank=True)
    status = models.CharField(max_length=30) # IN_PROGRESS, DONE, ABORTED
    fee = models.DecimalField(max_digits=9, decimal_places=2)
    total = models.DecimalField(max_digits=9, decimal_places=2)
    currency = models.CharField(max_length=10)

    CREATED = 'CREATED'
    CANCELED = 'CANCELED'
    CONFIRMED_WEB = 'CONFIRMED_WEB'
    CONFIRMED_IPN = 'CONFIRMED_IPN'
    FORGOTTEN = 'FORGOTTEN'
    
    CURRENCY_SYMBOLS = {'USD' : 'US$',
        'BRL' : 'R$'}

    @classmethod
    def newPayment(cls, offer):
        payment = cls()
        payment.offer = offer
        payment.creationDate = timezone.now()
        payment.lastChangeDate = payment.creationDate
        payment.status = Payment.CREATED
        payment.selectCurrency()
        payment.confirm_key = hashlib.md5(str(time.time()) + str(random.random())).hexdigest()
        return payment
    
    def selectCurrency(self):
        if(self.offer.sponsor.getUserInfo().brazilianPaypal):
            self.currency = 'BRL'
        else:
            self.currency = 'USD'
    
    def get_currency_symbol(self):
        return Payment.CURRENCY_SYMBOLS[self.currency]

    def setPaykey(self, paykey):
        self.paykey = paykey

    def getParts(self):
        return PaymentPart.objects.filter(payment=self)

    def is_confirmed(self):
        return self.status == Payment.CONFIRMED_WEB or self.status == Payment.CONFIRMED_IPN

    def cancel(self):
        event = PaymentHistEvent.newChangeEvent(payment=self, event=PaymentHistEvent.CANCEL)
        event.save()
        if(not self.is_confirmed()):
            self.status = Payment.CANCELED
            self.lastChangeDate = timezone.now()
            self.save()
        else:
            #TODO: logar coisas melhor
            print('warning: canceled confirmed payment %s'%self.id)

    def forget(self):
        event = PaymentHistEvent.newChangeEvent(payment=self, event=PaymentHistEvent.FORGET)
        event.save()
        if(self.status == Payment.CREATED):
            self.status = Payment.FORGOTTEN
            self.lastChangeDate = timezone.now()
            self.save()
        else:
            #TODO: logar coisas melhor
            print ('warning: forgot '+self.status+' payment %s'%self.id)

    def confirm_web(self):
        event = PaymentHistEvent.newChangeEvent(payment=self, event=PaymentHistEvent.CONFIRM_WEB)
        event.save()
        if(self.status != Payment.CONFIRMED_IPN):
            self.status = Payment.CONFIRMED_WEB
            self.lastChangeDate = timezone.now()
            self.save()
        if(self.status == Payment.CANCELED or self.status == Payment.CONFIRMED_WEB):
            #TODO: logar coisas melhor
            print ('warning: confirmed_web '+self.status+' payment %s'%self.id)

    def confirm_ipn(self):
        event = PaymentHistEvent.newChangeEvent(payment=self, event=PaymentHistEvent.CONFIRM_IPN)
        event.save()
        self.status = Payment.CONFIRMED_IPN
        self.lastChangeDate = timezone.now()
        self.save()
        if(self.status == Payment.CANCELED):
            #TODO: logar coisas melhor
            print ('warning: confirmed_ipn '+self.status+' payment %s'%self.id)

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
    price = models.DecimalField(max_digits=9, decimal_places=2)
    realprice = models.DecimalField(max_digits=9, decimal_places=2)

    @classmethod
    def newPart(cls, payment, solution, price, realprice):
        part = cls()
        part.payment = payment
        part.solution = solution
        part.programmer = solution.programmer
        part.paypalEmail = part.programmer.getUserInfo().paypalEmail
        part.price = Decimal(price)
        part.realprice = Decimal(realprice)
        return part
