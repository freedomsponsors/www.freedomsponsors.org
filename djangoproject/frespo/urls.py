from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.conf import settings
from django.views.generic import TemplateView
from registration.backends.default.views import RegistrationView
from core.forms import MyRegForm
from core.forms import FrespoPasswordResetForm


admin.autodiscover()

urlpatterns = []
if 'core' in settings.INSTALLED_APPS:
    urlpatterns += patterns('',
        # url(r'^.*$', TemplateView.as_view(template_name='core2/maintainance.html')),

        #from core.forms import RegistrationForm
        # url(r'^login/$',  'core.views.main_views.login'),
        # url(r'^logout/$', 'core.views.main_views.logout'),
        # url(r'^accounts/password/reset_done/$', 'core.views.registration_views.reset_password_done', name='password_reset_done'),
        # url(r'^/accounts/register/$', RegistrationView.as_view(form_class=RegistrationForm), name='registration_register'),
        # url(r'^accounts/password/reset/$', 'core.views.registration_views.reset_password'),
        # name='password_reset_confirm'),

        url(r'^logout$', 'django.contrib.auth.views.logout', {'next_page': '/'}),
        # url(r'^password_reset/$', 'django.contrib.auth.views.password_reset', {'password_reset_form': FrespoPasswordResetForm}, name='password_reset'),
        url(r'', include('django.contrib.auth.urls')),

        url(r'^accounts/password/reset/$', 'django.contrib.auth.views.password_reset', {'password_reset_form': FrespoPasswordResetForm}, name='password_reset'),
        url(r'^accounts/register/$', RegistrationView.as_view(form_class=MyRegForm), name='registration_register'),
        url(r'^accounts/', include('registration.backends.default.urls')),

        url(r'^$', 'core.views.main_views.home', name='home'),
        url(r'^rates$', 'core.views.main_views.rates', name='rates'),
        url(r'^404$', TemplateView.as_view(template_name='404.html')),
        url(r'^faq$', TemplateView.as_view(template_name='core2/faq.html')),
        url(r'^developers$', TemplateView.as_view(template_name='core2/developers.html')),
        url(r'^core/', include('core.urls')),
        url(r'^project/', include('core.urls.project_urls')),
        url(r'^issue/', include('core.urls.issue_urls')),
        url(r'^api/', include('core.urls.api_urls')),
        url(r'^myissues/', 'core.views.issue_views.myissues'),
        url(r'^offer/', include('core.urls.offer_urls')),
        url(r'^solution/', include('core.urls.solution_urls')),
        url(r'^search/', 'core.views.issue_views.listIssues'),
        url(r'^stats/',  'core.views.main_views.stats'),
        url(r'^spa$', TemplateView.as_view(template_name='spa.html')),
        url(r'^jslic$', TemplateView.as_view(template_name='core2/jslic.html')),
        url(r'^github-hook/', include('core.urls.github_hook_urls')),
        url(r'^feedback', include('core.urls.feedback_urls')),
        url(r'^user/', include('core.urls.user_urls')),
        url(r'^payment/', include('core.urls.payment_urls')),
        url(r'^sandbox/', include('sandbox.urls')),
        url(r'^github/', include('gh_frespo_integration.urls')),
        url(r'^bladmin/doc/', include('django.contrib.admindocs.urls')),
        url(r'^bladmin/', include(admin.site.urls)),
        url(r'^login-error/$', 'core.views.main_views.login_error'),
        url(r'^robots.txt$', TemplateView.as_view(template_name='core2/robots.txt', content_type='text/plain')),
        url(r'^sitemap.xml$', 'core.views.main_views.sitemap'),
        url('', include('social.apps.django_app.urls', namespace='social')),
        url(r'^email/$', 'core.views.user_views.redirect_to_user_page',
            {'email_verified': 'true'}, name='emailmgr_email_list'),
        url(r'^email/activate/(?P<identifier>\w+)/$',
            'emailmgr.views.email_activate',
            name='emailmgr_email_activate'
        ),
    )

urlpatterns += patterns('',
    url(r'^sandbox/', include('sandbox.urls')),
)

urlpatterns += staticfiles_urlpatterns()
# urlpatterns += feedback_urlpatterns
