from django.contrib import admin
from models import Device, Chunk


class DeviceAdmin(admin.ModelAdmin):
    pass
admin.site.register(Device, DeviceAdmin)


class DeviceInline(admin.TabularInline):
    model = Device
    extra = 0


class ChunkAdmin(admin.ModelAdmin):
    pass
admin.site.register(Chunk, ChunkAdmin)
