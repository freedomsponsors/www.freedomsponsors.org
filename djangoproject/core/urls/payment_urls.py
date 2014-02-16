from django.conf.urls import patterns, url

urlpatterns = patterns('core.views.payment_views',
                       url(r'^$', 'list_payments'),
                       )
