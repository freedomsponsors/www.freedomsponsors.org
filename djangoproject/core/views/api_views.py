import json
from django.http.response import HttpResponse
from core.models import Project
from core.services import stats_services
from django.core.exceptions import ObjectDoesNotExist

def get_project(request, project_id):
    try:
        project = Project.objects.get(pk=project_id)
        result = project.to_dict_json()
        result['stats'] = _replace_decimals_stats(stats_services.project_stats(project))
        return HttpResponse(json.dumps(result), content_type='application/json')
    except ObjectDoesNotExist:
        return HttpResponse(json.dumps({'error': 'Project not found'}), status=404, content_type='application/json')
	

#def get_project(request, project_id):
#    project = Project.objects.get(pk=project_id)
#    if not project:
#        return HttpResponse(json.dumps({'error': 'Project not found'}), status=404, content_type='application/json')
#    result = project.to_dict_json()
#    result['stats'] = _replace_decimals_stats(stats_services.project_stats(project))
#    return HttpResponse(json.dumps(result), content_type='application/json')


def _replace_decimals_stats(stats):
    stats['btc_open'] = float(stats['btc_open'])
    stats['btc_paid'] = float(stats['btc_paid'])
    stats['usd_open'] = float(stats['usd_open'])
    stats['usd_paid'] = float(stats['usd_paid'])
    stats['total_btc'] = float(stats['total_btc'])
    stats['total_usd'] = float(stats['total_usd'])
    return stats
