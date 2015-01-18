from django.contrib import admin
from apps.push.admin import DeviceInline
from models import User


class UserAdmin(admin.ModelAdmin):
    date_hierarchy = '_created_at'
    list_display = ('image_tag', 'name', 'email', 'is_admin', 'is_active', )
    readonly_fields = ('image_tag_big',)
    list_editable = ('is_active', )
    list_filter = ('is_admin', 'is_active', )
    # list_select_related = ('devices', 'likes_from', 'likes_to')
    search_fields = ('name', 'email', )
    inlines = (DeviceInline, )

admin.site.register(User, UserAdmin)
