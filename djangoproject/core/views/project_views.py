from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from core.models import Project

__author__ = 'tony'


def view(request, project_id):
    project = Project.objects.get(pk=project_id)
    return render_to_response('core2/project.html',
                              {'project': project},
                              context_instance=RequestContext(request))


def edit_form(request, project_id):
    project = Project.objects.get(pk=project_id)
    return render_to_response('core2/project_edit.html',
                              {'project': project},
                              context_instance=RequestContext(request))


def edit(request):
    project_id = int(request.POST.get('id'))
    project = Project.objects.get(pk=project_id)
    if 'image3x1' in request.FILES and request.FILES['image3x1']:
        project.image3x1 = request.FILES['image3x1']
        project.save()
    return redirect('/core/project/%s' % project.id)


def list(request):
    projects = Project.objects.all()
    projects = projects.order_by('name')
    return render_to_response('core/project_list.html',
        {'projects':projects},
        context_instance = RequestContext(request))