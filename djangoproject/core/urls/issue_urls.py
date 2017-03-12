from django.conf.urls import url
from core.views import issue_views
from core.views import comment_views

urlpatterns = [
    url(r'^rss$', issue_views.listIssuesFeed),
    url(r'^sponsor/submit$', issue_views.sponsorIssue),
    url(r'^sponsor$', issue_views.addIssueForm),
    url(r'^add/submit$', issue_views.addIssue),
    url(r'^kickstart/submit$', issue_views.kickstartIssue),
    url(r'^add/$', issue_views.addIssueForm),
    url(r'^edit/submit$', issue_views.editIssue),
    url(r'^(?P<issue_id>\d+)/$', issue_views.viewIssue),
    url(r'^(?P<issue_id>\d+)/.*$', issue_views.viewIssue),
]

urlpatterns += [
    url(r'^comment/add/submit$', comment_views.addIssueComment),
    url(r'^comment/edit/submit$', comment_views.editIssueComment),
    url(r'^comment/(?P<comment_id>\d+)/history$', comment_views.viewIssueCommentHistory),
]
