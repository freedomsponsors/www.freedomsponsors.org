from django.template import  RequestContext
from django.shortcuts import render_to_response, redirect
from gh_frespo_integration.services import github_services
from django.contrib.auth.decorators import login_required

@login_required
def configure(request):
    repos = github_services.get_repos_and_configs(request.user)
    return render_to_response('github/configure.html',
        {"repos" : repos},
        context_instance = RequestContext(request))

@login_required
def configure_submit(request):
    github_services.update_user_configs(request.user, request.POST)
    return redirect('/github/configure')


