from django.conf.urls import url, patterns, include
from django.contrib import admin
from django.conf import settings

if 'djrill' in settings.INSTALLED_APPS:
    from djrill import DjrillAdminSite
    admin.site = DjrillAdminSite()

admin.autodiscover()

urlpatterns = patterns('',
    (r'^auth/', include('apps.auth.urls')),
    (r'^push/', include('apps.push.urls')),
    (r'^users/', include('apps.users.urls')),
    (r'^likes/', include('apps.likes.urls')),
    (r'^multimedia/', include('apps.multimedia.urls')),
    (r'^debug_gps/', include('apps.debug_gps.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^logs/', include('logtailer.urls')),
)

from django.conf import settings
if settings.DEBUG:
    urlpatterns += patterns('',
        #Debug media files service:
        (r'^'+settings.MEDIA_URL+'(?P<path>.*)$', 'django.views.static.serve',
        {'document_root':
            settings.MEDIA_ROOT,
            'show_indexes': True}),
    )
