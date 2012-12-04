from django.core import mail
from mailer.management.commands import send_mail
from django.core.mail.backends import locmem

__author__ = 'tony'

def send_emails():
	cmd = send_mail.Command()
	cmd.handle_noargs()

def clear_sent():
    mail.outbox = []

def assert_sent_count(testcase, count):
    msg = 'sent %s emails instead of %s :\n' % (len(mail.outbox), count)
    for message in mail.outbox:
        msg += '\tTO: '+str(message.to) + ' / SUBJECT: '+message.subject+'\n'
    testcase.assertEquals(count, len(mail.outbox), msg)

def assert_sent(testcase, to, subject):
    found = False
    emails = ''
    for message in mail.outbox:
        if(to == message.to[0] and subject == message.subject):
            found = True
            break
        emails += '\tTO: '+str(message.to) + ' / SUBJECT: '+message.subject+'\n'
    err = 'email [TO: '+to + ' / SUBJECT: '+subject+'] not found in sent mail list:\n'+emails
    testcase.assertTrue(found, err)