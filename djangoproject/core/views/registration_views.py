__author__ = 'tony'

from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.hashers import UNUSABLE_PASSWORD, is_password_usable, get_hasher


class CustomResetForm(PasswordResetForm):

    def clean_email(self):
        """
        Validates that an active user exists with the given email address.
        """
        email = self.cleaned_data["email"]
        self.users_cache = User.objects.filter(email__iexact=email,
                                               is_active=True)
        if not len(self.users_cache):
            raise forms.ValidationError(self.error_messages['unknown'])
        for user in self.users_cache:
            if user.password == UNUSABLE_PASSWORD:
                raise forms.ValidationError(self.error_messages['unusable'] + 'This happens because the user account was '
                    'created with an OpenID or OAuth provider (tipically Google, Facebook, MyOpenID, etc). '
                    'Try logging in with a login provider (see http://freedomsponsors.org/core/user/%s)' % user.id)
        return email


def reset_password(request):
    return auth_views.password_reset(request, password_reset_form=CustomResetForm)