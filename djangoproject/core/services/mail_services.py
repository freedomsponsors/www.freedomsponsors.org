from core.models import *
from django.template.loader import get_template
from django.template import Context
from core.utils.frespo_utils import send_html_mail
from django.conf import settings
from core.utils.frespo_utils import twoplaces

ADMINS_EMAILS = map((lambda x: x[1]), settings.ADMINS)

def plain_send_mail(to, subject, body):
    send_html_mail(subject, body, body, settings.DEFAULT_FROM_EMAIL, [to])

def send_mail_to_all_users(subject, body):
    count = 0
    for user in User.objects.all():
        if(user.getUserInfo() and user.getUserInfo().receiveAllEmail):
            plain_send_mail(user.email, subject, body)
            count += 1
    return count

def _send_mail_to_user(user, subject, templateName, contextData):
    if(user.getUserInfo() and user.getUserInfo().receiveAllEmail):
        template = get_template(templateName)
        context = Context(contextData)
        html_content = template.render(context)
        send_html_mail(subject, html_content, html_content, settings.DEFAULT_FROM_EMAIL, [user.email])

def notifyWatchers_workbegun(solution, comment, watches):
    def send_func(watch):
        if(watch.user.id != solution.programmer.id):
            _send_mail_to_user(user = watch.user,
                subject = solution.programmer.getUserInfo().screenName+" has just begun working on issue [%s]"%solution.issue.title,
                templateName = 'email/workbegun.html',
                contextData = {"solution" : solution,
                               "you" : watch.user,
                               "SITE_HOME" : settings.SITE_HOME,
                               "comment" : comment})
    _notify_watchers(send_func, watches)

def notifyWatchers_acceptingpayments(solution, watches):
    def send_func(watch):
        if(watch.user.id != solution.programmer.id):
            _send_mail_to_user(user = watch.user,
                subject = solution.programmer.getUserInfo().screenName+" is ready to accept payments for issue [%s]"%solution.issue.title,
                templateName = 'email/acceptingpayments.html',
                contextData = {"solution" : solution,
                               "you" : watch.user,
                               "SITE_HOME" : settings.SITE_HOME,})
    _notify_watchers(send_func, watches)


def welcome(user):
    _send_mail_to_user(user=user,
        subject='Welcome to FreedomSponsors',
        templateName='email/welcome.html',
        contextData={"you" : user})

def notifyWatchers_workstopped(solution, comment, watches):
    def send_func(watch):
        if(watch.user.id != solution.programmer.id):
            _send_mail_to_user(user = watch.user,
                subject = solution.programmer.getUserInfo().screenName+" has stopped working on issue [%s]"%solution.issue.title,
                templateName = 'email/workstopped.html',
                contextData = {"solution" : solution,
                               "you" : watch.user,
                               "SITE_HOME" : settings.SITE_HOME,
                               "comment" : comment})
    _notify_watchers(send_func, watches)

def notifyWatchers_workdone(solution, comment, watches):
    def send_func(watch):
        if(watch.user.id != solution.programmer.id):
            _send_mail_to_user(user = watch.user,
                subject = solution.programmer.getUserInfo().screenName+" resolved issue [%s]"%solution.issue.title,
                templateName = 'email/workdone.html',
                contextData = {"theirSolution" : solution,
                               "you" : watch.user,
                               "SITE_HOME" : settings.SITE_HOME,
                               "comment" : comment})
    _notify_watchers(send_func, watches)

#    for otherSolution in solution.issue.getSolutions():
#        if(not solution.id == otherSolution.id):

def notifyWatchers_offerrevoked(offer, comment, watches):
    def send_func(watch):
        if(watch.user.id != offer.sponsor.id):
            _send_mail_to_user(user = watch.user,
                subject = "%s revoked his %s %s offer for issue [%s]" % (
                    offer.sponsor.getUserInfo().screenName,
                    offer.get_currency_symbol(),
                    str(twoplaces(offer.price)),
                    offer.issue.title
                ),
                templateName = 'email/offerrevoked.html',
                contextData = {"you" : watch.user,
                               "offer" : offer,
                               "SITE_HOME" : settings.SITE_HOME,
                               "comment" : comment})
    _notify_watchers(send_func, watches)

def notifyWatchers_offeradded(offer, watches):
    def send_func(watch):
        if(watch.user.id != offer.sponsor.id):
            _send_mail_to_user(user = watch.user,
                subject = "%s made a %s %s offer for issue [%s]" % (
                    offer.sponsor.getUserInfo().screenName,
                    offer.get_currency_symbol(),
                    str(offer.price),
                    offer.issue.title
                ),
                templateName = 'email/offeradded.html',
                contextData = {"you" : watch.user,
                               "theirOffer" : offer,
                               "SITE_HOME" : settings.SITE_HOME})
    _notify_watchers(send_func, watches)

def notifyWatchers_offerchanged(old_offer, new_offer, watches):
    action = 'changed'
    if new_offer.currency == old_offer.currency and new_offer.price > old_offer.price:
        action = 'raised'
    elif new_offer.currency == old_offer.currency and new_offer.price < old_offer.price:
        action = 'lowered'
    elif(not new_offer.acceptanceCriteria == old_offer.acceptanceCriteria):
        action = 'changed the acceptance criteria for'

    if(action):
        def send_func(watch):
            if(watch.user.id != new_offer.sponsor.id):
                _send_mail_to_user(user = watch.user,
                    subject = old_offer.sponsor.getUserInfo().screenName+" "+action+" the "+old_offer.get_currency_symbol()+" "+str(twoplaces(old_offer.price))+" offer on issue [%s]"%old_offer.issue.title,
                    templateName = 'email/offerchanged.html',
                    contextData = {"you" : watch.user,
                                   "old_offer" : old_offer,
                                   "new_offer" : new_offer,
                                   "action" : action,
                                   "SITE_HOME" : settings.SITE_HOME})
        _notify_watchers(send_func, watches)

def notify_payment_parties_and_watchers_paymentconfirmed(payment, watches):
    already_sent_to = {}
    for part in payment.getParts():
        _send_mail_to_user(user = part.programmer, 
            subject = payment.offer.sponsor.getUserInfo().screenName+" has made you a "+payment.get_currency_symbol()+" "+str(twoplaces(part.price))+" payment",
            templateName = 'email/payment_received.html',
            contextData = {"payment" : payment,
            "part" : part,
            "SITE_HOME" : settings.SITE_HOME})
        already_sent_to[part.programmer.email] = True
    _send_mail_to_user(user = payment.offer.sponsor,
        subject = "You have made a "+payment.get_currency_symbol()+" "+str(twoplaces(payment.total))+" payment",
        templateName = 'email/payment_sent.html',
        contextData = {"payment" : payment,
        "SITE_HOME" : settings.SITE_HOME})
    already_sent_to[payment.offer.sponsor.email] = True
    def send_func(watch):
        subject = "%s has paid his offer [%s %s / %s]" % (
            payment.offer.sponsor.getUserInfo().screenName,
            payment.offer.get_currency_symbol(),
            str(twoplaces(payment.offer.price)),
            payment.offer.issue.title)
        contextData = {"you": watch.user,
                       "issue": payment.offer.issue,
                       "offer": payment.offer,
                       "SITE_HOME": settings.SITE_HOME,}
        _send_mail_to_user(watch.user, subject, 'email/payment_made.html', contextData)
    _notify_watchers(send_func, watches, already_sent_to)


def notifyWatchers_newissuecomment(comment, watches):
    def send_func(watch):
        if(watch.user.id != comment.author.id):
            subject = "%s added a comment on issue [%s]"%(comment.author.getUserInfo().screenName, comment.issue.title)
            contextData = {"you" : watch.user,
                           "issue" : comment.issue,
                           "comment" : comment,
                           "SITE_HOME" : settings.SITE_HOME,
                           "type" : "issue"}
            _send_mail_to_user(watch.user, subject, 'email/comment_added.html', contextData)
    _notify_watchers(send_func, watches)

def notifyWatchers_newoffercomment(comment, watches):
    def send_func(watch):
        if(watch.user.id != comment.author.id):
            subject = "%s added a comment on offer [%S %s / %s]" % (
                comment.author.getUserInfo().screenName,
                comment.offer.get_currency_symbol(),
                str(twoplaces(comment.offer.price)),
                comment.offer.issue.title)
            contextData = {"you": watch.user,
                           "issue": comment.offer.issue,
                           "offer": comment.offer,
                           "comment": comment,
                           "SITE_HOME": settings.SITE_HOME,
                           "type": "offer"}
            _send_mail_to_user(watch.user, subject, 'email/comment_added.html', contextData)
    _notify_watchers(send_func, watches)

def _notify_watchers(send_func, watches, already_sent_to = None):
    if not already_sent_to:
        already_sent_to = {}
    for watch in watches:
        if(not already_sent_to.has_key(watch.user.email)):
            send_func(watch)
            already_sent_to[watch.user.email] = True

def notify_admin(subject, msg):
    send_html_mail(subject, msg, msg, settings.DEFAULT_FROM_EMAIL, ADMINS_EMAILS)
