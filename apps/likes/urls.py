from django.conf.urls import patterns, url

from views import LikesView, LikesListView, LikesFromView, LikesFromListView, LikesBroadcastView

urlpatterns = patterns('',
    url(r'^broadcast/$', LikesBroadcastView.as_view(), name='likes'),

    url(r'^from/$', LikesFromListView.as_view(), name='likes_from_list'),
    url(r'^from/(?P<id>\d*)/$', LikesFromView.as_view(), name='likes_from'),

    url(r'^$', LikesListView.as_view(), name='likes_list'),
    url(r'^(?P<id>\d*)/$', LikesView.as_view(), name='likes'),

    url(r'^(?P<id>\d*)$', LikesView.as_view(), name='likes'),  # Deprecated
)
