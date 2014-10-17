from django.conf.urls import patterns, url

from views import PositionsView, PositionView
from libs.decorators import is_admin_or_forbiden

urlpatterns = patterns('',
    url(r'positions/(?P<id>\d+)$', is_admin_or_forbiden(PositionView.as_view())),
    url(r'positions/$', is_admin_or_forbiden(PositionsView.as_view(), ignore_methods=["POST"])),
    #url(r'^login/$', AuthView.as_view()),
    #url(r'^map/$', MapView.as_view()),
)
