from django.contrib import admin
from models import ReferrerProfile, Referred


class ReferrerProfileAdmin(admin.ModelAdmin):
    date_hierarchy = 'created_at'
    list_display = ('user', 'active', 'accepted_referrals_count', 'total_referrals_count', )
    list_editable = ('active', )
    list_filter = ('active', )
    list_select_related = ('user', 'referrals', )
    # search_fields = ('token', 'user.name', 'user.email', )

admin.site.register(ReferrerProfile, ReferrerProfileAdmin)


class ReferredAdmin(admin.ModelAdmin):
    list_display = ('user', 'referrer', 'accepted', 'IP', 'created_at', )
    list_editable = ('accepted', )
    list_filter = ('accepted', 'referrer', )
    list_select_related = ('user', 'referrer', )
admin.site.register(Referred, ReferredAdmin)
