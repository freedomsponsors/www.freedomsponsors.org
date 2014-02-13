import json

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


@csrf_exempt
def hook(request, token):
    if request.method == 'POST':
        return HttpResponse(json.dumps(request.POST))
    return HttpResponse('OK')
