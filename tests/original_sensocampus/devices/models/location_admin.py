from django.contrib import admin

from devices.models.device_admin import DeviceInline


class BuildingAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'topic')


class LocationAdmin(admin.ModelAdmin):
    list_display = ('location_building', 'room', 'topic')
    readonly_fields = ('topic', )
    inlines = (DeviceInline, )

    def location_building(self, obj):
        return obj.building.name

    def location_room(self, obj):
        return obj.room

    location_building.admin_order_field = 'building__name'
