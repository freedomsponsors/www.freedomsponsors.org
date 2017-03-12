from django.conf.urls import url
from core.views import github_hook_views

urlpatterns = [
    url(r'^(?P<token>\w+)/$', github_hook_views.hook),
]
