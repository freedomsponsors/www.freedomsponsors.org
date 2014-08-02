from django import forms
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.hashers import UNUSABLE_PASSWORD_PREFIX
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from registration.forms import RegistrationForm as _RegistrationForm

class RegistrationForm(_RegistrationForm):

    def clean_email(self):
        """
        Validate that the email is not already
        in use.
        """
        existing = User.objects.filter(email__iexact=self.cleaned_data['email'])
        if existing.exists():
            raise forms.ValidationError(_("A user with that email already exists."))
        else:
            return self.cleaned_data['email']

    def clean_password1(self):
        """
        Validate that the email is not already
        in use.
        """
        password = self.cleaned_data['password1']
        if len(password) < 6:
            raise forms.ValidationError(_("We won't lecture you on password security - you probably heard enough about it by now. But please make it at least 6 characters long!"))
        else:
            return self.cleaned_data['password1']


class FrespoPasswordResetForm(PasswordResetForm):
    def clean_email(self):
        """
        Validates that an active user exists with the given email address.
        """
        email = self.cleaned_data["email"]
        self.users_cache = User.objects.filter(email__iexact=email,
                                               is_active=True)
        if not len(self.users_cache):
            raise forms.ValidationError('User not found')
        for user in self.users_cache:
            if user.password.startswith(UNUSABLE_PASSWORD_PREFIX):
                raise forms.ValidationError('Error: password not set. This happens because the user account was '
                    'created with an OpenID or OAuth provider (tipically Google, Facebook, MyOpenID, etc). '
                    'Try logging in with your login provider (see http://freedomsponsors.org%s)' % user.get_view_link())
        return email
