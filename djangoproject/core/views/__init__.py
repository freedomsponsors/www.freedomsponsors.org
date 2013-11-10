__author__ = 'tony'


def is_old_layout(request):
    return False
    # return 'old_layout' in request.session


def template_folder(request):
    return 'core2/'
    # if is_old_layout(request):
    #     return 'core/'
    # else:
    #     return 'core2/'

HOME_CRUMB = {
    'link': '/',
    'name': 'Home'
}