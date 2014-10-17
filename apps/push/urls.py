from django.conf.urls import patterns, url

from views import subscribe, unsubscribe, sync  # , test_push
# from views import test_push

urlpatterns = patterns('django_server.views',
    url(r'^subscribe/$', subscribe, name='subscribe'),
    url(r'^unsubscribe/$', unsubscribe, name='unsubscribe'),
    url(r'^sync/$', sync, name='sync'),

    #For testing:
    # url(r'^test_push/$', test_push, name='test_push'),
)
