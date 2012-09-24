from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
import registration

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'core.views.main_views.home', name='home'),
    # url(r'^frespo/', include('frespo.foo.urls')),
    url(r'^core/', include('core.urls')),

    url(r'^bladmin/doc/', include('django.contrib.admindocs.urls')),

    url(r'^bladmin/', include(admin.site.urls)),

    url(r'^accounts/', include('registration.backends.default.urls')),

    url(r'', include('social_auth.urls')),
    url(r'', include('emailmgr.urls')),
)

urlpatterns += staticfiles_urlpatterns()
# urlpatterns += feedback_urlpatterns
