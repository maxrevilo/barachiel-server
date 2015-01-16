from django.contrib import admin
from models import Confirmation


class ConfirmationAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'token', 'created_at', )

admin.site.register(Confirmation, ConfirmationAdmin)
