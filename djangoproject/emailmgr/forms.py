from models import EmailAddress
from django.forms import ModelForm, ValidationError
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

class EmailAddressForm(ModelForm):
    def __init__(self, user=None, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.user = user

    class Meta:
        model = EmailAddress
        exclude = ('user', 'is_primary', 'is_active', 'is_activation_sent', 'identifier')

    def clean_email(self):
        """
        Ensure this email address is unique throughout the ``site`` identified by SITE_ID.
        """
        email = self.cleaned_data['email']
        try:
            EmailAddress.objects.get(user=self.user, email=email)
        except EmailAddress.DoesNotExist:
            try:
                User.objects.get(email=email)
            except User.DoesNotExist:
                return email
        
        raise ValidationError(u"This email address already in use.")

    def save(self):
        e = EmailAddress(**{'user': self.user, 'email': self.cleaned_data["email"]})
        return e.save()



