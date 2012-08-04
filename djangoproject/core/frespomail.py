from core.models import *
from django.template.loader import get_template
from django.template import Context
from mailer import send_html_mail
from django.conf import settings

ADMINS_EMAILS = map((lambda x: x[1]), settings.ADMINS)

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
			subject = offer.sponsor.getUserInfo().screenName+" revoked his U$ "+str(offer.price)+" offer for an issue that you are involved with",
			templateName = 'email/offerrevoked.html', 
			contextData = {"solution" : solution,
			"offer" : offer,
			"SITE_HOME" : settings.SITE_HOME,
			"comment" : comment})

def notifyProgrammers_offeradded(offer):
	for solution in offer.issue.getSolutions():
		_send_mail_to_user(user = solution.programmer, 
			subject = offer.sponsor.getUserInfo().screenName+" made a U$ "+str(offer.price)+" offer for an issue that you are involved with",
			templateName = 'email/offeradded_programmer.html', 
			contextData = {"solution" : solution,
			"offer" : offer,
			"SITE_HOME" : settings.SITE_HOME})

def notifySponsors_offeradded(offer):
	for otherOffer in offer.issue.getOffers():
		if(not offer.id == otherOffer.id):
			_send_mail_to_user(user = otherOffer.sponsor, 
				subject = offer.sponsor.getUserInfo().screenName+" made a U$ "+str(offer.price)+" offer for an issue that you're sponsoring",
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
				subject = old_offer.sponsor.getUserInfo().screenName+" "+action+" the U$ "+str(old_offer.price)+" offer on an issue that you are involved with",
				templateName = 'email/offerchanged.html', 
				contextData = {"old_offer" : old_offer,
				"new_offer" : new_offer,
				"solution" : solution,
				"action" : action,
				"SITE_HOME" : settings.SITE_HOME})

def notifyProgrammers_paymentconfirmed(payment):
	for part in payment.getParts():
		_send_mail_to_user(user = part.programmer, 
			subject = payment.offer.sponsor.getUserInfo().screenName+" has made you a U$ "+str(part.price)+" payment",
			templateName = 'email/offerpaid.html', 
			contextData = {"payment" : payment,
			"part" : part,
			"SITE_HOME" : settings.SITE_HOME})
		
def notifyProgrammers_newissuecomment(comment):
	for solution in comment.issue.getSolutions():
		if (comment.author.id != solution.programmer.id):
			_send_mail_to_user(user = solution.programmer, 
				subject = comment.author.getUserInfo().screenName+" commented on issue ["+comment.issue.title+"]",
				templateName = 'email/comment_added.html', 
				contextData = {"you" : solution.programmer,
				"issue" : comment.issue,
				"comment" : comment,
				"type" : "issue",
				"SITE_HOME" : settings.SITE_HOME})

def notifySponsors_newissuecomment(comment):
	for offer in comment.issue.getOffers():
		if (comment.author.id != offer.sponsor.id):
			_send_mail_to_user(user = offer.sponsor, 
				subject = comment.author.getUserInfo().screenName+" commented on issue ["+comment.issue.title+"]",
				templateName = 'email/comment_added.html', 
				contextData = {"you" : offer.sponsor,
				"issue" : comment.issue,
				"comment" : comment,
				"SITE_HOME" : settings.SITE_HOME,
				"type" : "issue"})

def notifyProgrammers_newoffercomment(comment):
	for solution in comment.offer.issue.getSolutions():
		if (comment.author.id != solution.programmer.id):
			_send_mail_to_user(user = solution.programmer, 
				subject = comment.author.getUserInfo().screenName+" commented on issue offer ["+comment.issue.title+"]",
				templateName = 'email/comment_added.html', 
				contextData = {"you" : solution.programmer,
				"issue" : comment.offer.issue,
				"comment" : comment,
				"type" : "offer",
				"SITE_HOME" : settings.SITE_HOME})

def notifySponsors_newoffercomment(comment):
	for offer in comment.offer.issue.getOffers():
		if (comment.author.id != offer.sponsor.id):
			_send_mail_to_user(user = offer.sponsor, 
				subject = comment.author.getUserInfo().screenName+" commented on issue ["+comment.issue.title+"]",
				templateName = 'email/comment_added.html', 
				contextData = {"you" : offer.sponsor,
				"issue" : comment.offer.issue,
				"comment" : comment,
				"SITE_HOME" : settings.SITE_HOME,
				"type" : "issue"})

def notify_admin(subject, msg):
	send_html_mail(subject, msg, msg, settings.DEFAULT_FROM_EMAIL, ADMINS_EMAILS)
