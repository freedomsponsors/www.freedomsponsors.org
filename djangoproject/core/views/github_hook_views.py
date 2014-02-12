# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


@csrf_exempt
def hook(request, token):
    if request.method == 'POST':
        return HttpResponse(request.POST.get('payload'))
    return HttpResponse('OK')
