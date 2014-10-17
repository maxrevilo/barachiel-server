from django.conf.urls import patterns, url

from views import LikesView

urlpatterns = patterns('',
    url(r'^(?P<id>\d*)$', LikesView.as_view(), name='likes'),
)
