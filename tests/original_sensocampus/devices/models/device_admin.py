from django.db import models
from django.contrib import admin
from django.contrib import messages
from django.db.models.signals import m2m_changed
from django.http import HttpResponse, HttpResponseRedirect

from devices.models.device import Device, on_locations_update_device
from devices.models.log_message import LogMessage
from devices.models.permission import PermissionInline
from devices.models.log_message import LogMessageInline
from devices.tasks.device import *


# TODO: fix
class DeviceInline(admin.TabularInline):
    model = Device.locations.through
    extra = 0


class DeviceAdmin(admin.ModelAdmin):
    list_display = ('mac', 'description', 'type', 'last_update', 'last_status', 'enabled', 'credentials_delivered')
    readonly_fields = ('last_update', 'last_status', 'login', 'password', 'credentials_delivered')
    exclude = ()
    actions = ('revoke_credentials', 'update', 'reset', 'reboot', 'status', 'restart',)
    inlines = (PermissionInline,)
    filter_horizontal = ('locations', )

    def revoke_credentials(self, request, queryset):
        queryset.update(credentials_delivered=False)
        for dev in queryset:
            dev.reset_credentials()
            dev.save()

    revoke_credentials.short_description = "Revoke selected devices credentials"

    def update(self, request, queryset):
        for dev in queryset:
            update_device.delay(dev.id)

    update.short_description = "Update device configuration"

    def reset(self, request, queryset):
        for dev in queryset:
            reset_device.delay(dev.id)

    reset.short_description = "Reset device configuration"

    def restart(self, request, queryset):
        for dev in queryset:
            restart_device.delay(dev.id)

    restart.short_description = "Restart device application"

    def reboot(self, request, queryset):
        for dev in queryset:
            reboot_device.delay(dev.id)

    reboot.short_description = "Reboot device"

    def status(self, request, queryset):
        for dev in queryset:
            status_device.delay(dev.id)

    status.short_description = "Request device status"

m2m_changed.connect(on_locations_update_device, sender=Device.locations.through)
