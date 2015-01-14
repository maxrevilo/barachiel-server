from django.conf.urls import patterns, url

from views import (
    login,
    signup,
    logout,
    reset_password,
    change_password,
    email_confirm,
    EmailConfirmTokenView
)
#from django.views.decorators.csrf import csrf_exempt

# HTML Requests
urlpatterns = patterns('',
    url(r'^login/$', login, name='login'),

    url(r'^signup/$', signup, name='signup'),

    url(r'^logout/$', logout, name='logout'),

    url(r'^reset_password/$', reset_password, name='reset_password'),

    url(r'^change_password/$', change_password, name='change_password'),

    url(r'^confirm_email/$', email_confirm, name='email_confirm_reminder'),

    url(r'^confirm_email/user/(?P<id>\d+|me)/token/(?P<token>.+)/$', EmailConfirmTokenView.as_view(), name='email_confirm_token'),
)
