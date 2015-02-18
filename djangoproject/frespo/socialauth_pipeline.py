from django.conf import settings
from social.exceptions import AuthException


def associate_by_email(backend, details, user=None, *args, **kwargs):
    backend_fullname = backend.__module__+"."+backend.__class__.__name__
    if not backend_fullname in settings.SOCIALAUTH_PIPELINE_TRUSTED_BACKENDS:
        return None
    if user:
        return None

    email = details.get('email')
    if email:
        # Try to associate accounts registered with the same email address,
        # only if it's a single object. AuthException is raised if multiple
        # objects are returned.
        users = list(backend.strategy.storage.user.get_users_by_email(email))
        if len(users) == 0:
            return None
        elif len(users) > 1:
            raise AuthException(
                backend,
                'The given email address is associated with another account'
            )
        else:
            return {'user': users[0]}
