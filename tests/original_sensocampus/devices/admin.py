from django.contrib import admin

from devices.models.device import Device, Type, TypeAdmin
from devices.models.device_admin import DeviceAdmin
from devices.models.location import Location, Building
from devices.models.location_admin import LocationAdmin, BuildingAdmin
from devices.models.log_message import LogMessage, LogMessageAdmin

admin.site.register(Device, DeviceAdmin)
admin.site.register(Type, TypeAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Building, BuildingAdmin)
admin.site.register(LogMessage, LogMessageAdmin)
