from exceptions import BaseException
from django.shortcuts import redirect

# This is not used anywhere.
# Im leaving it here just to serve as an example of how to write a decorator
def complete_registration_first(view_func):
	def _decorated(request, *args, **kwargs):
		if(request.user.is_authenticated()):
			user = request.user
			if(user.is_registration_complete()):
				return view_func(request, *args, **kwargs)
			else:
				return redirect('/core/user/edit?next='+request.get_full_path())
				#TODO
		else:
			raise BaseException('decorator complete_registration_first invoked on unauthenticated session')
	return _decorated