from django.conf.urls import patterns, url

from views import LikesView, LikesListView

urlpatterns = patterns('',
    url(r'^$', LikesListView.as_view(), name='likes_list'),

    url(r'^(?P<id>\d*)/$', LikesView.as_view(), name='likes'),
    url(r'^(?P<id>\d*)$', LikesView.as_view(), name='likes'),  # Deprecated
)
