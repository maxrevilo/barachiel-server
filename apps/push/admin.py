from django.contrib import admin
from models import Device, Chunk


class DeviceAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user', 'last_sync')
admin.site.register(Device, DeviceAdmin)


class DeviceInline(admin.TabularInline):
    model = Device
    extra = 0


class ChunkAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'devices_number', 'expiration', 'created_at')
admin.site.register(Chunk, ChunkAdmin)
