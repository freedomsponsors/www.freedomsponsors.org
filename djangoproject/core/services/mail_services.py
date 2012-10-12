from core.models import *
from django.template.loader import get_template
from django.template import Context
from mailer import send_html_mail
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


def notifySponsors_workbegun(solution, comment):
    for offer in solution.issue.getOffers():
        _send_mail_to_user(user = offer.sponsor, 
            subject = solution.programmer.getUserInfo().screenName+" has just begun working on your sponsored issue",
            templateName = 'email/workbegun.html', 
            contextData = {"solution" : solution,
            "offer" : offer,
            "SITE_HOME" : settings.SITE_HOME,
            "comment" : comment})

def notifySponsors_workstopped(solution, comment):
    for offer in solution.issue.getOffers():
        _send_mail_to_user(user = offer.sponsor, 
            subject = solution.programmer.getUserInfo().screenName+" has stopped working on your sponsored issue",
            templateName = 'email/workstopped.html', 
            contextData = {"solution" : solution,
            "offer" : offer,
            "SITE_HOME" : settings.SITE_HOME,
            "comment" : comment})

def notifySponsors_workdone(solution, comment):
    for offer in solution.issue.getOffers():
        _send_mail_to_user(user = offer.sponsor, 
            subject = solution.programmer.getUserInfo().screenName+" resolved your sponsored issue",
            templateName = 'email/workdone_sponsor.html', 
            contextData = {"solution" : solution,
            "offer" : offer,
            "SITE_HOME" : settings.SITE_HOME,
            "comment" : comment})

def notifyProgrammers_workdone(solution, comment):
    for otherSolution in solution.issue.getSolutions():
        if(not solution.id == otherSolution.id):
            _send_mail_to_user(user = otherSolution.programmer, 
                subject = solution.programmer.getUserInfo().screenName+" resolved an issue that you are involved with",
                templateName = 'email/workdone_programmer.html', 
                contextData = {"theirSolution" : solution,
                "yourSolution" : otherSolution,
                "SITE_HOME" : settings.SITE_HOME,
                "comment" : comment})

def notifyProgrammers_offerrevoked(offer, comment):
    for solution in offer.issue.getSolutions():
        _send_mail_to_user(user = solution.programmer, 
            subject = offer.sponsor.getUserInfo().screenName+" revoked his US$ "+str(offer.price)+" offer for an issue that you are involved with",
            templateName = 'email/offerrevoked.html', 
            contextData = {"solution" : solution,
            "offer" : offer,
            "SITE_HOME" : settings.SITE_HOME,
            "comment" : comment})

def notifyProgrammers_offeradded(offer):
    for solution in offer.issue.getSolutions():
        _send_mail_to_user(user = solution.programmer, 
            subject = offer.sponsor.getUserInfo().screenName+" made a US$ "+str(offer.price)+" offer for an issue that you are involved with",
            templateName = 'email/offeradded_programmer.html', 
            contextData = {"solution" : solution,
            "offer" : offer,
            "SITE_HOME" : settings.SITE_HOME})

def notifySponsors_offeradded(offer):
    for otherOffer in offer.issue.getOffers():
        if(not offer.id == otherOffer.id):
            _send_mail_to_user(user = otherOffer.sponsor, 
                subject = offer.sponsor.getUserInfo().screenName+" made a US$ "+str(offer.price)+" offer for an issue that you're sponsoring",
                templateName = 'email/offeradded_sponsor.html', 
                contextData = {"yourOffer" : otherOffer,
                "theirOffer" : offer,
                "SITE_HOME" : settings.SITE_HOME})

def notifyProgrammers_offerchanged(old_offer, new_offer):
    action = ''
    if(new_offer.price > old_offer.price):
        action = 'raised'
    elif(new_offer.price < old_offer.price):
        action = 'lowered'
    elif(not new_offer.acceptanceCriteria == old_offer.acceptanceCriteria):
        action = 'changed the acceptance criteria for'

    if(action):
        for solution in new_offer.issue.getSolutions():
            _send_mail_to_user(user = solution.programmer, 
                subject = old_offer.sponsor.getUserInfo().screenName+" "+action+" the US$ "+str(old_offer.price)+" offer on an issue that you are involved with",
                templateName = 'email/offerchanged.html', 
                contextData = {"old_offer" : old_offer,
                "new_offer" : new_offer,
                "solution" : solution,
                "action" : action,
                "SITE_HOME" : settings.SITE_HOME})

def notify_payment_parties_paymentconfirmed(payment):
    for part in payment.getParts():
        _send_mail_to_user(user = part.programmer, 
            subject = payment.offer.sponsor.getUserInfo().screenName+" has made you a "+payment.get_currency_symbol()+" "+str(twoplaces(part.price))+" payment",
            templateName = 'email/payment_received.html',
            contextData = {"payment" : payment,
            "part" : part,
            "SITE_HOME" : settings.SITE_HOME})
    _send_mail_to_user(user = payment.offer.sponsor,
        subject = "You have made a "+payment.get_currency_symbol()+" "+str(twoplaces(payment.total))+" payment",
        templateName = 'email/payment_sent.html',
        contextData = {"payment" : payment,
        "SITE_HOME" : settings.SITE_HOME})
        
def notifyWatchers_newissuecomment(comment, watches):
    for watch in watches:
        if(watch.user.id != comment.author.id):
            subject = "%s added a comment on issue [%s]"%(comment.author.getUserInfo().screenName, comment.issue.title)
            contextData = {"you" : watch.user,
                "issue" : comment.issue,
                "comment" : comment,
                "SITE_HOME" : settings.SITE_HOME,
                "type" : "issue"}
            _send_mail_to_user(watch.user, subject, 'email/comment_added.html', contextData)

def notifyWatchers_newoffercomment(comment, watches):
    already_sent_to = {}
    for watch in watches:
        if(watch.user.id != comment.author.id and not already_sent_to.has_key(watch.user.email)):
            subject = "%s added a comment on offer [US$ %s / %s]"%(comment.author.getUserInfo().screenName, str(twoplaces(comment.offer.price)), comment.offer.issue.title)
            contextData = {"you" : watch.user,
                "issue" : comment.offer.issue,
                "offer" : comment.offer,
                "comment" : comment,
                "SITE_HOME" : settings.SITE_HOME,
                "type" : "offer"}
            _send_mail_to_user(watch.user, subject, 'email/comment_added.html', contextData)
            already_sent_to[watch.user.email] = True

def notify_admin(subject, msg):
    send_html_mail(subject, msg, msg, settings.DEFAULT_FROM_EMAIL, ADMINS_EMAILS)
