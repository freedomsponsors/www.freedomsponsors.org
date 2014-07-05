from django.conf.urls import patterns, url

urlpatterns = patterns('core.views.issue_views',
    url(r'^rss$', 'listIssuesFeed'),
    url(r'^sponsor/submit$', 'sponsorIssue'),
    url(r'^sponsor$', 'addIssueForm'),
    url(r'^add/submit$', 'addIssue'),
    url(r'^kickstart/submit$', 'kickstartIssue'),
    url(r'^add/$', 'addIssueForm'),
    url(r'^edit/submit$', 'editIssue'),
    url(r'^(?P<issue_id>\d+)/$', 'viewIssue'),
    url(r'^(?P<issue_id>\d+)/.*$', 'viewIssue'),
)

urlpatterns += patterns('core.views.comment_views',
    url(r'^comment/add/submit$', 'addIssueComment'),
    url(r'^comment/edit/submit$', 'editIssueComment'),
    url(r'^comment/(?P<comment_id>\d+)/history$', 'viewIssueCommentHistory'),
)
