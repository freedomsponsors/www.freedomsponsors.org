from django.http.response import HttpResponse


def only_post(view_func):
    def _decorated(request, *args, **kwargs):
        if request.method.lower() != 'post':
            return HttpResponse(status=400, content='Only post allowed here')
        else:
            return view_func(request, *args, **kwargs)
    return _decorated
