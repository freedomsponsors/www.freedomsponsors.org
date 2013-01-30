from exceptions import BaseException
from django.shortcuts import redirect
from django.contrib import messages
from django.utils import translation

class CompleteRegistrationFirst:
    def process_request(self, request):
        if(request.user.is_authenticated()):
            if(request.path in ['/core/user/edit', '/core/user/edit/submit']):
                return None
            user = request.user
            if(user.is_registration_complete()):
                return None
            else:
                messages.info(request, 'Please complete your profile before proceeding.')
                return redirect('/core/user/edit?next='+request.get_full_path())
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

