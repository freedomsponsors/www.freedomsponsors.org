from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
# TODO: remove core dependency
from core.forms import RegistrationForm
from core.urls import watch_urls

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'core.views.main_views.home', name='home'),
    url(r'^core/', include('core.urls')),
    url(r'^sandbox/', include('sandbox.urls')),
    url(r'^github/', include('gh_frespo_integration.urls')),
    url(r'^bladmin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^bladmin/', include(admin.site.urls)),
    url(r'^/accounts/register/$', 'registration.views.register', {
        'backend': 'registration.backends.default.DefaultBackend',
        'form_class': RegistrationForm
    }, name='registration_register'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'', include('social_auth.urls')),
    url(r'^email/$', 'core.views.user_views.redirect_to_user_page',
        {'email_verified': 'true'}, name='emailmgr_email_list'),
    url(r'^email/activate/(?P<identifier>\w+)/$',
        'emailmgr.views.email_activate',
        name='emailmgr_email_activate'
    ),
)

urlpatterns += watch_urls.urlpatterns

urlpatterns += staticfiles_urlpatterns()
# urlpatterns += feedback_urlpatterns
