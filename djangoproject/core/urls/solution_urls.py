from django.conf.urls import patterns, url

urlpatterns = patterns('core.views.issue_views',
    url(r'^add/submit$', 'addSolution'),
    url(r'^abort/submit$', 'abortSolution'),
    url(r'^resolve/submit$', 'resolveSolution'),
)
