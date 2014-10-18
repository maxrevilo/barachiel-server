from django.contrib import admin
from models import Like


class LikeAdmin(admin.ModelAdmin):
    pass

admin.site.register(Like, LikeAdmin)
