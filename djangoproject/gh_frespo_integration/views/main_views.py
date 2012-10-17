from django.template import  RequestContext
from django.shortcuts import render_to_response, redirect
from gh_frespo_integration.services import github_services
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def configure(request):
    try:
        repos = github_services.get_repos_and_configs(request.user)
    except BaseException as e:
        repos = []
        messages.error(request, 'Cannot list repos: '+e.message)
    return render_to_response('github/configure.html',
        {"repos" : repos},
        context_instance = RequestContext(request))

@login_required
def configure_submit(request):
    try:
        github_services.update_user_configs(request.user, request.POST)
    except BaseException as e:
        repos = []
        messages.error(request, 'Cannot save config repos: '+e.message)
    return redirect('/github/configure')


