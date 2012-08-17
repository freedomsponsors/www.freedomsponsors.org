from exceptions import BaseException
from django.shortcuts import redirect

class CompleteRegistrationFirst:
	def process_request(self, request):
		if(request.user.is_authenticated()):
			if(request.path == '/core/user/edit'):
				return None
			user = request.user
			if(user.is_registration_complete()):
				return None
			else:
				return redirect('/core/user/edit?next='+request.get_full_path())
		else:
			return None


