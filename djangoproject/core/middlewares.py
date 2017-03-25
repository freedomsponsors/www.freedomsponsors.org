from django.shortcuts import render, redirect
from django.contrib import messages
from django.template.context import RequestContext
from django.utils import translation
from django.core.urlresolvers import reverse
import logging
logger = logging.getLogger(__name__)


class FSPreconditionsMiddleware:
    def process_request(self, request):
        user = request.user
        if user.is_authenticated() and not user.is_active:
            if request.path != '/logout':
                return render(request, 'core2/account_disabled.html', {})
        if user.is_authenticated() and not user.is_registration_complete():
            whitelist = [
                'editUserForm',
                'editUser',
            ]
            whitelist2 = [
                '/core/json/check_username_availability'
            ]
            _paths = [reverse(v) for v in whitelist] + whitelist2
            for p in _paths:
                if p in request.path:
                    return None

            messages.info(request, 'Please complete your profile before proceeding.')
            url = reverse('editUserForm')
            return redirect('%s?next=%s' % (url, request.get_full_path()))
        else:
            return None


class Translation(object):
    def process_request(self, request):
        language = "en"
        if request.user.is_authenticated():
            userinfo = request.user.getUserInfo()
            if userinfo and userinfo.preferred_language_code:
                language = userinfo.preferred_language_code
        translation.activate(language)
        request.LANGUAGE_CODE = translation.get_language()


class ErrorMiddleware(object):
    """
    Alter HttpRequest objects on Error
    """
    def process_exception(self, request, exception):
        """
        Add user details.
        """
        user = request.user
        if user.is_authenticated():
            request.META['USER'] = "%s / %s" % (request.user.id, request.user.username)
        else:
            request.META['USER'] = "Unauthenticated"
