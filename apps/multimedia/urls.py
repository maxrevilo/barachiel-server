from django.conf.urls import patterns, url

from views import MediaUser #, MediaInstance

urlpatterns = patterns('',
    #url(r'^(?P<id>\d+)$',
    #    MediaInstance.as_view(),
    #    name='media_instance'),

    url(r'^user/$',
        MediaUser.as_view(),
        name='media_user'),
)
