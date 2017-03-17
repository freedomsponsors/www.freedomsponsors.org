import json
from django.http import HttpResponse
# from django.shortcuts import render_to_response, redirect
from django.shortcuts import render, redirect
from django.template import RequestContext
from core.decorators import only_post
from core.models import Project, ActionLog
from core.services import stats_services, issue_services, watch_services, mail_services
from django.contrib.auth.decorators import login_required

__author__ = 'tony'


def view(request, project_id):
    try:
        project = Project.objects.get(pk=project_id)
    except:
        return HttpResponse(status=404, content='Project not found')
    if project.redirectto_project:
        do_redirect = 'false' != request.GET.get('redirect')
        if do_redirect:
            return redirect(project.redirectto_project.get_view_link())

    stats = stats_services.project_stats(project)
    issues_sponsoring = issue_services.search_issues(project_id=project_id, is_sponsored=True)[0:3]
    issues_kickstarting = issue_services.search_issues(project_id=project_id, is_sponsored=False)[0:3]
    issues_sponsoring = json.dumps(issue_services.to_card_dict(issues_sponsoring))
    issues_kickstarting = json.dumps(issue_services.to_card_dict(issues_kickstarting))
    top_sponsors = stats_services.project_top_sponsors(project_id)[0:5]
    top_programmers = stats_services.project_top_programmers(project_id)[0:5]
    is_watching = request.user.is_authenticated() and watch_services.is_watching_project(request.user, project.id)
    return render('core2/project.html',
                              {'project': project,
                               'stats': stats,
                               'tags': json.dumps([t.name for t in project.get_tags()]),
                               'issues_sponsoring': issues_sponsoring,
                               'issues_kickstarting': issues_kickstarting,
                               'top_sponsors': top_sponsors,
                               'top_programmers': top_programmers,
                               'is_watching': is_watching,
                               })


@login_required
def edit_form(request, project_id):
    project = Project.objects.get(pk=project_id)
    return render('core2/project_edit.html',
                              {'project': project})


@login_required
@only_post
def edit(request):
    project_id = int(request.POST.get('id'))
    project = Project.objects.get(pk=project_id)
    old_json = project.to_json()
    if 'image3x1' in request.FILES and request.FILES['image3x1']:
        project.image3x1 = request.FILES['image3x1']
    project.description = request.POST.get('description')
    project.homeURL = request.POST.get('homeURL')
    project.save()
    watches = watch_services.find_project_watches(project)
    mail_services.notifyWatchers_project_edited(request.user, project, old_json, watches)
    ActionLog.log_edit_project(project=project, user=request.user, old_json=old_json)
    return redirect('core.views.project_views.view', project_id=project.id)


def list(request):
    projects = Project.objects.all()
    projects = projects.order_by('name')
    return render('core2/project_list.html',
        {'projects':projects})