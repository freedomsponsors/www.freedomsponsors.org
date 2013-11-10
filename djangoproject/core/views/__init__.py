__author__ = 'tony'


def is_old_layout(request):
    return 'old_layout' in request.session


def template_folder(request):
    if is_old_layout(request):
        return 'core/'
    else:
        return 'core2/'

HOME_CRUMB = {
    'link': '/',
    'name': 'Home'
}