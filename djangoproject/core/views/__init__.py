__author__ = 'tony'


def is_new_layout(request):
    return 'new_layout' in request.session


def template_folder(request):
    if is_new_layout(request):
        return 'core2/'
    else:
        return 'core/'