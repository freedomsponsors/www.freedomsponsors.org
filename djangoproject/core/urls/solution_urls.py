from django.conf.urls import url
from core.views import issue_views


urlpatterns = [
    url(r'^add/submit$', issue_views.addSolution),
    url(r'^abort/submit$', issue_views.abortSolution),
    url(r'^resolve/submit$', issue_views.resolveSolution),
]
