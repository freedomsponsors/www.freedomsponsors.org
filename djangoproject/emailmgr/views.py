from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib import messages as Msg
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from forms import EmailAddressForm
from models import EmailAddress
from utils import send_activation, get_template, sort_email
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from signals import user_added_email, user_sent_activation, user_activated_email

@login_required
def email_add(request):
    """
    User is logged and has a primary email address already
    This will add an aditional email address to this User
    """
    if request.method == 'POST':
        form = EmailAddressForm(user=request.user, data=request.POST)
        if form.is_valid():
            email = form.save()
            user_added_email.send(sender=EmailAddress, email_address=email)
            Msg.add_message (request, Msg.SUCCESS, _('email address added'))
            form = EmailAddressForm(user=request.user)
    else:
        form = EmailAddressForm(user=request.user)
    emails_list = EmailAddress.objects.filter(user=request.user).order_by(*sort_email())
    return render_to_response(get_template('emailmgr_email_list.html'),
                              {
                                'email_list': emails_list,
                                'email_form': form
                              },
                              context_instance=RequestContext(request)
                              )

@login_required
def email_make_primary(request, identifier="somekey"):
    """
    User is logged in, has a second email that is already activated and 
    wants to make that the primary email address.
    The User objects' email address will also be replace with this newly
    primary email address, so Django internals work it the new primary address too
    """
    email = get_object_or_404(EmailAddress, identifier__iexact=identifier.lower())
    if email.is_active:
        if email.is_primary:
            Msg.add_message (request, Msg.SUCCESS, _('email address is already primary'))
        else:
            emails = EmailAddress.objects.filter(user=email.user)
            for e in emails:
                e.is_primary = False
                e.save()
    
            email.user.email = email.email
            email.user.save()
            email.is_primary = True
            email.save()
            Msg.add_message (request, Msg.SUCCESS, _('primary address changed'))
    else:
        Msg.add_message (request, Msg.SUCCESS, _('email address must be activated first'))

    return HttpResponseRedirect(reverse('emailmgr_email_list'))


@login_required
def email_send_activation(request, identifier="somekey"):
    """
    The user is logged in, has added a new email address to his/her account.
    User can do anything with the newly added email, unless it is first activated.
    This function will send an activation email to the currently primary email address 
    associated with the User's account
    """
    email = get_object_or_404(EmailAddress, identifier__iexact=identifier.lower())
    if email.is_active:
        Msg.add_message (request, Msg.SUCCESS, _('email address already activated'))
    else:
        send_activation(email, request.is_secure())
        email.is_activation_sent = True
        email.save()
        user_sent_activation.send(sender=EmailAddress, email_address=email)
        Msg.add_message (request, Msg.SUCCESS, _('activation email sent'))

    return HttpResponseRedirect(reverse('emailmgr_email_list'))


@login_required
def email_activate(request, identifier="somekey"):
    """
    User is already logged in and the activation link will trigger the email address
    in question to be activated. If the account is already active, then a message is 
    put in the message buffer indicating that the email is already active
    """
    try:
        email = EmailAddress.objects.get(identifier__iexact=identifier.lower())
    except EmailAddress.DoesNotExist:
        Msg.add_message (request, Msg.ERROR, _('email address not found'))
    else:
        if email.is_active:
            Msg.add_message (request, Msg.SUCCESS, _('email address already active'))
        else:
            email.is_active = True
            if not email.user.email:
                email.user.email = email.email
                email.is_primary = True
                email.user.save()
            email.save()
            user_activated_email.send(sender=EmailAddress, email_address=email)
            Msg.add_message (request, Msg.SUCCESS, _('email address is now active'))
            
    return HttpResponseRedirect(reverse('emailmgr_email_list'))

@login_required
def email_delete(request, identifier="somekey"):
    """
    Email needs to be removed from User's account, primary email address cannot be removed
    """
    email = get_object_or_404(EmailAddress, identifier__iexact=identifier.lower())
    if email.email == request.user.email:
        Msg.add_message (request, Msg.ERROR, _('cannot remove primary email address'))
    elif email.user != request.user:
        Msg.add_message (request, Msg.ERROR, _('email address is not associated with this account'))
    else:
        email.delete()
        Msg.add_message (request, Msg.SUCCESS, _('email address removed'))

    return HttpResponseRedirect(reverse('emailmgr_email_list'))


@login_required
def email_list(request):
    """
    All email address associated with User account will be passed into the template as a list
    An ``add`` email form will be passed in the template so user can add new email inline
    """
    form = EmailAddressForm(user=request.user)
    emails_list = EmailAddress.objects.filter(user=request.user).order_by(*sort_email())
    return render_to_response(get_template('emailmgr_email_list.html'),
                              {
                                'email_list': emails_list,
                                'email_form': form
                              },
                              context_instance=RequestContext(request)
                              )










