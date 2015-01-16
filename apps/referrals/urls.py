from django.conf.urls import patterns, url

from views import ReferralsListView

urlpatterns = patterns('',
    url(r'^$', ReferralsListView.as_view(), name='referrals_list'),
)
