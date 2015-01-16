from django.contrib import admin
from models import ReferrerProfile


class ReferrerProfileAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    list_display = ('user', 'active', )
    list_editable = ('active', )
    list_filter = ('active', )
    # list_select_related = ('devices', 'likes_from', 'likes_to')
    search_fields = ('token', 'user.name', 'user.email', )

admin.site.register(ReferrerProfile, ReferrerProfileAdmin)
