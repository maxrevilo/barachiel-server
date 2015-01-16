from django.contrib import admin
from models import Like


class LikeAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'anonymous', '_created_at')

admin.site.register(Like, LikeAdmin)
