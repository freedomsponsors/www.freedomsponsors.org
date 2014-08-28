import json
import logging
import html2text

from django.core.mail import EmailMultiAlternatives
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from core.models import *
from django.template.loader import get_template
from django.template import Context
from django.conf import settings
from core.utils.frespo_utils import twoplaces

logger = logging.getLogger(__name__)

ADMINS_EMAILS = map((lambda x: x[1]), settings.ADMINS)


def plain_send_mail(to, subject, body, from_email=settings.DEFAULT_FROM_EMAIL):
    send_html_mail(subject, body, body, from_email, [to])


def send_html_mail(subject, body_txt, body_html, from_email, to_addresses):
    try:
        for to_addr in to_addresses:
            validate_email(to_addr)
    except ValidationError:
        logger.warn('Email not sent. Invalid email address in %s. subject = %s' % (to_addresses, subject))
        return
    msg = EmailMultiAlternatives(subject, body_txt, from_email, to_addresses)
    msg.attach_alternative(body_html, "text/html")
    msg.send()


def send_mail_to_all_users(subject, body, from_email=settings.DEFAULT_FROM_EMAIL):
    count = 0
    for user in User.objects.filter(is_active=True):
        if user.is_active and user.getUserInfo() and user.getUserInfo().receiveEmail_announcements:
            try:
                plain_send_mail(user.email, subject, body, from_email)
                count += 1
            except BaseException, e:
                logger.error('cannot send mail to user %s' % user.id)
                logger.exception(e)

    return count


def _send_mail_to_user(user, subject, templateName, contextData, whentrue, even_when_inactive=False):
    if (user.is_active or even_when_inactive) and user.getUserInfo() and (not whentrue or getattr(user.getUserInfo(), whentrue)):
        template = get_template(templateName)
        context = Context(contextData)
        html_content = template.render(context)
        text_content = html2text.html2text(html_content)
        send_html_mail(subject, text_content, html_content, settings.DEFAULT_FROM_EMAIL, [user.email])


def notifyWatchers_workbegun(solution, comment, watches):
    def send_func(watch):
        if watch.user.id != solution.programmer.id:
            _send_mail_to_user(
                user=watch.user,
                subject=solution.programmer.username+" has just begun working on issue [%s]" % solution.issue.title,
                templateName='email/workbegun.html',
                contextData={"solution": solution,
                             "you": watch.user,
                             "SITE_HOME": settings.SITE_HOME,
                             "comment": comment},
                whentrue='receiveEmail_issue_work'
            )
    _notify_watchers(send_func, watches)


def notifyWatchers_project_edited(user, project, old_json, watches):
    old_dic = json.loads(old_json)
    changed_description = old_dic['description'] != project.description
    changed_image = project.image3x1 and old_dic['image3x1'] != project.image3x1.url
    def send_func(watch):
        if watch.user.id != user.id:
            _send_mail_to_user(user=watch.user,
                               subject=user.username + " edited project [%s]" % project.name,
                               templateName='email/project_edited.html',
                               contextData={"project": project,
                                            "user": user,
                                            "you": watch.user,
                                            "SITE_HOME": settings.SITE_HOME,
                                            "changed_description": changed_description,
                                            "changed_image": changed_image,
                                            "old_dic": old_dic},
                               whentrue='receiveEmail_issue_work')
    _notify_watchers(send_func, watches)


def notifyWatchers_project_tag_added(user, project, tag, watches):
    def send_func(watch):
        if watch.user.id != user.id:
            _send_mail_to_user(user=watch.user,
                               subject=user.username + " added the tag [%s] to project [%s]" % (tag, project.name),
                               templateName='email/project_tag_added.html',
                               contextData={"project": project,
                                            "user": user,
                                            "you": watch.user,
                                            "SITE_HOME": settings.SITE_HOME,
                                            "tag": tag,
                                            },
                               whentrue='receiveEmail_issue_work')
    _notify_watchers(send_func, watches)


def notifyWatchers_project_tag_removed(user, project, tag, watches):
    def send_func(watch):
        if watch.user.id != user.id:
            _send_mail_to_user(user=watch.user,
                               subject=user.username + " removed tag [%s] from project [%s]" % (tag, project.name),
                               templateName='email/project_tag_removed.html',
                               contextData={"project": project,
                                            "user": user,
                                            "you": watch.user,
                                            "SITE_HOME": settings.SITE_HOME,
                                            "tag": tag,
                                            },
                               whentrue='receiveEmail_issue_work')
    _notify_watchers(send_func, watches)


def notifyWatchers_acceptingpayments(solution, watches):
    def send_func(watch):
        if(watch.user.id != solution.programmer.id):
            _send_mail_to_user(user = watch.user,
                subject = solution.programmer.username+" is ready to accept payments for issue [%s]"%solution.issue.title,
                templateName = 'email/acceptingpayments.html',
                contextData = {"solution" : solution,
                               "you" : watch.user,
                               "SITE_HOME" : settings.SITE_HOME,},
                whentrue='receiveEmail_issue_work')
    _notify_watchers(send_func, watches)


def welcome(user):
    _send_mail_to_user(
        user=user,
        subject='Welcome to FreedomSponsors',
        templateName='email/welcome.html',
        contextData={"you": user},
        whentrue=None
    )


def deactivated(user):
    _send_mail_to_user(
        user=user,
        subject='Your account has been deactivated',
        templateName='email/farewell.html',
        contextData={"you": user},
        whentrue=None,
        even_when_inactive=True
    )


def notifyWatchers_workstopped(solution, comment, watches):
    def send_func(watch):
        if(watch.user.id != solution.programmer.id):
            _send_mail_to_user(user = watch.user,
                subject = solution.programmer.username+" has stopped working on issue [%s]"%solution.issue.title,
                templateName = 'email/workstopped.html',
                contextData = {"solution" : solution,
                               "you" : watch.user,
                               "SITE_HOME" : settings.SITE_HOME,
                               "comment" : comment},
                whentrue='receiveEmail_issue_work')
    _notify_watchers(send_func, watches)


def notifyWatchers_workdone(solution, comment, watches):
    def send_func(watch):
        if(watch.user.id != solution.programmer.id):
            _send_mail_to_user(user = watch.user,
                subject = solution.programmer.username+" resolved issue [%s]"%solution.issue.title,
                templateName = 'email/workdone.html',
                contextData = {"theirSolution" : solution,
                               "you" : watch.user,
                               "SITE_HOME" : settings.SITE_HOME,
                               "comment" : comment},
                whentrue='receiveEmail_issue_work')
    _notify_watchers(send_func, watches)

#    for otherSolution in solution.issue.getSolutions():
#        if(not solution.id == otherSolution.id):


def notifyWatchers_offerrevoked(offer, comment, watches):
    def send_func(watch):
        if(watch.user.id != offer.sponsor.id):
            _send_mail_to_user(user = watch.user,
                subject = "%s revoked his %s %s offer for issue [%s]" % (
                    offer.sponsor.username,
                    offer.get_currency_symbol(),
                    str(twoplaces(offer.price)),
                    offer.issue.title
                ),
                templateName = 'email/offerrevoked.html',
                contextData = {"you" : watch.user,
                               "offer" : offer,
                               "SITE_HOME" : settings.SITE_HOME,
                               "comment" : comment},
                whentrue='receiveEmail_issue_offer')
    _notify_watchers(send_func, watches)


def notifyWatchers_offeradded(offer, watches):
    def send_func(watch):
        if(watch.user.id != offer.sponsor.id):
            _send_mail_to_user(user = watch.user,
                subject = "%s made a %s %s offer for issue [%s]" % (
                    offer.sponsor.username,
                    offer.get_currency_symbol(),
                    str(offer.price),
                    offer.issue.title
                ),
                templateName = 'email/offeradded.html',
                contextData = {"you" : watch.user,
                               "theirOffer" : offer,
                               "SITE_HOME" : settings.SITE_HOME},
                whentrue='receiveEmail_issue_offer')
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
                _send_mail_to_user(
                    user = watch.user,
                    subject = old_offer.sponsor.username+" "+action+" the "+old_offer.get_currency_symbol()+" "+str(twoplaces(old_offer.price))+" offer on issue [%s]"%old_offer.issue.title,
                    templateName = 'email/offerchanged.html',
                    contextData = {"you" : watch.user,
                                   "old_offer": old_offer,
                                   "new_offer": new_offer,
                                   "action": action,
                                   "SITE_HOME": settings.SITE_HOME},
                    whentrue='receiveEmail_issue_offer'
                )
        _notify_watchers(send_func, watches)


def notify_payment_parties_and_watchers_paymentconfirmed(payment, watches):
    already_sent_to = {}
    for part in payment.getParts():
        _send_mail_to_user(
            user = part.programmer,
            subject=payment.offer.sponsor.username+" has made you a "+payment.get_currency_symbol()+" "+str(twoplaces(part.price))+" payment",
            templateName='email/payment_received.html',
            contextData={"payment" : payment,
            "part" : part,
            "SITE_HOME": settings.SITE_HOME},
            whentrue=None,
            even_when_inactive=True,
        )
        already_sent_to[part.programmer.email] = True
    _send_mail_to_user(
        user=payment.offer.sponsor,
        subject="You have made a "+payment.get_currency_symbol()+" "+str(twoplaces(payment.total))+" payment",
        templateName='email/payment_sent.html',
        contextData={"payment": payment, "SITE_HOME": settings.SITE_HOME},
        whentrue=None,
        even_when_inactive=True,
    )
    already_sent_to[payment.offer.sponsor.email] = True
    def send_func(watch):
        subject = "%s has paid his offer [%s %s / %s]" % (
            payment.offer.sponsor.username,
            payment.offer.get_currency_symbol(),
            str(twoplaces(payment.offer.price)),
            payment.offer.issue.title)
        contextData = {"you": watch.user,
                       "issue": payment.offer.issue,
                       "offer": payment.offer,
                       "SITE_HOME": settings.SITE_HOME,}
        _send_mail_to_user(user = watch.user,
            subject = subject,
            templateName = 'email/payment_made.html',
            contextData = contextData,
            whentrue='receiveEmail_issue_payment')
    _notify_watchers(send_func, watches, already_sent_to)


def notifyWatchers_newissuecomment(comment, watches):
    def send_func(watch):
        if(watch.user.id != comment.author.id):
            subject = "%s added a comment on issue [%s]"%(comment.author.username, comment.issue.title)
            contextData = {"you" : watch.user,
                           "issue" : comment.issue,
                           "comment" : comment,
                           "SITE_HOME" : settings.SITE_HOME,
                           "type" : "issue"}
            _send_mail_to_user(user = watch.user,
                subject = subject,
                templateName = 'email/comment_added.html',
                contextData = contextData,
                whentrue='receiveEmail_issue_comments')
    _notify_watchers(send_func, watches)


def notifyWatchers_newoffercomment(comment, watches):
    def send_func(watch):
        if watch.user.id != comment.author.id:
            subject = "%s added a comment on offer [%s %s / %s]" % (
                comment.author.username,
                comment.offer.get_currency_symbol(),
                str(twoplaces(comment.offer.price)),
                comment.offer.issue.title)
            contextData = {"you": watch.user,
                           "issue": comment.offer.issue,
                           "offer": comment.offer,
                           "comment": comment,
                           "SITE_HOME": settings.SITE_HOME,
                           "type": "offer"}
            _send_mail_to_user(
                user=watch.user,
                subject=subject,
                templateName='email/comment_added.html',
                contextData=contextData,
                whentrue='receiveEmail_issue_comments'
            )
    _notify_watchers(send_func, watches)


def notify_bitcoin_payment_was_sent_to_programmers_and_is_waiting_confirmation(payment):
    parts = PaymentPart.objects.filter(payment__id=payment.id)
    contextData = {'you': payment.offer.sponsor,
                   'payment': payment,
                   'parts': parts}
    template = get_template('email/bitcoin_payment_was_sent_to_programmers_and_is_waiting_confirmation.html')
    context = Context(contextData)
    html_content = template.render(context)
    text_content = html2text.html2text(html_content)
    subject = 'BTC %s payment received, and forwarded to programmer. Wating confirmation.' % payment.total_bitcoin_received
    send_html_mail(subject, text_content, html_content, settings.DEFAULT_FROM_EMAIL, [payment.offer.sponsor.email])
    adm_subject = '[ADMIN NOTIFY] %s' % subject
    notify_admin(adm_subject, html_content)


def _notify_watchers(send_func, watches, already_sent_to = None):
    if not already_sent_to:
        already_sent_to = {}
    for watch in watches:
        if not already_sent_to.has_key(watch.user.email):
            send_func(watch)
            already_sent_to[watch.user.email] = True


def notify_admin(subject, msg):
    send_html_mail(subject, msg, msg, settings.DEFAULT_FROM_EMAIL, ADMINS_EMAILS)
