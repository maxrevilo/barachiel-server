from django.conf.urls import patterns, url

from views import UsersInstanceView, UsersListView, UsersPrivacyView

urlpatterns = patterns('',
    url(r'^$', UsersListView.as_view(), name='user_list'),

    url(r'^(?P<id>\d+|me)$', UsersInstanceView.as_view(), name='user'),

    url(r'^privacy$', UsersPrivacyView.as_view(), name='user_privacy'),
)
