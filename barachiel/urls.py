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
    (r'^referrals/', include('apps.referrals.urls')),
    (r'^likes/', include('apps.likes.urls')),
    (r'^multimedia/', include('apps.multimedia.urls')),
    (r'^debug_gps/', include('apps.debug_gps.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^logs/', include('logtailer.urls')),

    # WARN: DJANGO_RQ with "RQ_SHOW_ADMIN_LINK = True" might override the admin template
    (r'^django-rq/', include('django_rq.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        # Debug media files service:
        (r'^'+settings.MEDIA_URL+'(?P<path>.*)$', 'django.views.static.serve',
        {'document_root':
            settings.MEDIA_ROOT,
            'show_indexes': True}),
    )
