from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from utils import get_unique_random
from django.db.models import signals

class EmailAddress(models.Model):

    user = models.ForeignKey(User, related_name="%(class)s")
    email = models.EmailField(_("Email Address"))
    is_primary = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_activation_sent = models.BooleanField(default=False)
    identifier = models.CharField(max_length=255, null=True)

    class Meta:
        verbose_name = _("email address")
        verbose_name_plural = _("email addresses")
        unique_together = (("user", "email"),)

    def __unicode__(self):
        return u"%s (%s)" % (self.email, self.user.username)

    def save(self, *args, **kwargs):
        if not self.identifier:
            self.identifier = get_unique_random(20).lower()
        super(EmailAddress, self).save(*args, **kwargs)


#########################################################
# stick signals listeners here to do some work for us
#########################################################
def create_primary_email_for_new_user(sender, instance, created, **kwargs):
    """
    Create a matching email address seperate from that of User object when a user object is created.
    """
    # user was just created, so no worries about duplicate emails as it has been done before
    if instance.email:
        try:
            EmailAddress.objects.get(user=instance, email__iexact=instance.email)
        except EmailAddress.DoesNotExist:
            e = EmailAddress(**{'user': instance, 
                                'email': instance.email, 
                                'is_primary': True,
                                'is_active': True})
            e.save()

def remove_all_emails_for_deleted_user(sender, instance, **kwargs):
    """
    Delete all emails addresses associated with this user that was just delete.
    """
    # user was just delete, delete any email associated with this user
    emails = EmailAddress.objects.filter(user=instance)
    for e in emails:
        e.delete()

# latch on signals here
signals.post_save.connect(create_primary_email_for_new_user, sender=User)
signals.post_delete.connect(remove_all_emails_for_deleted_user, sender=User)
