from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from registration.forms import RegistrationForm as _Form

class RegistrationForm(_Form):

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
