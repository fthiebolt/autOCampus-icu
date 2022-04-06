###############################################################################
#
# neOCampus
#
# class: device model
#
# description: contains definition of all fields related to each device. This
#   model specifies table 'device' of database 'sensOCampus'
#
# F.Thiebolt    [oct.17] corrected mqtt connexion failure
#               added fields 'server' and 'port' to a device
# T.Bueno       [may.16] initial release 
#
from django.db import models
from django.contrib import admin
from django.conf import settings
from django.db.models.signals import m2m_changed, post_save, pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError

from uuid import uuid4
import re
import json

from devices.utils import sanitize_string, validate_mac, format_mac
from devices.models.location import Location
from devices.models.permission import Permission, PermissionInline


#
# Type of a device (e.g RPi2, RPi3, Pi0W, esp32 ...)
# Note: created online by users
class Type(models.Model):
    name = models.CharField(max_length=64, blank=False, null=False, unique=True)
    description = models.CharField(max_length=2048, blank=True, null=True)

    def __str__(self):
        return '%s' % self.name


class TypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', )


class Device(models.Model):
    mac = models.CharField(max_length=17, blank=False, null=False, unique=True, verbose_name="MAC address",
                           validators=[validate_mac])
    type = models.ForeignKey(Type, null=False, blank=False, verbose_name="Device type")
    description = models.CharField(max_length=2048, blank=True, null=True)
    locations = models.ManyToManyField(Location)
    last_update = models.DateTimeField(blank=True, null=True)
    last_status = models.CharField(max_length=128, blank=True, null=True)
    enabled = models.BooleanField(default=True, blank=False)
    login = models.CharField(max_length=128, blank=True, unique=True, verbose_name="login")
    password = models.CharField(max_length=128, blank=True, verbose_name="password")

    modules = models.TextField(blank=False, null=False, default="[]", max_length=16768,
                               verbose_name="Modules configuration")

    credentials_delivered = models.BooleanField(default=False, blank=False)

    # [oct.17] add per-device 'server' and 'port'. Reason is that we need to use a different
    # port when abroad (from UT3 networks)
    mqtt_defaults = models.BooleanField(default=True, blank=False);     # devices normaly make use of default MQTT server and default MQTT port
    mqtt_server = models.CharField(max_length=128, blank=True, null=True, verbose_name="MQTT server")
    mqtt_port = models.PositiveSmallIntegerField( blank=True, null=True, verbose_name="MQTT port")


    def __str__(self):
        if self.description:
            return '%s (%s)' % (self.mac, self.description)
        else:
            return '%s' % self.mac

    def reset_credentials(self):
        self.login = settings.LOGIN_PREFIX + sanitize_string(self.mac).replace("_", "")
        self.password = str(uuid4())

    def clean(self):
        self.mac = format_mac(self.mac)

        if not self.login or not self.password:
            self.reset_credentials()

        if self.modules:
            try:
                test = json.loads(self.modules)
            except json.JSONDecodeError as ex:
                raise ValidationError("This field should be a valid JSON string, or be empty: " + str(ex))

            else:
                import validictory

                conf_schema = {"type": "array", "items": {"type": "object", "properties": {"modules": {"type": "array", "items": {"type": "object", "properties": {"module": {"type": "string"}, "unit": {"type": "string"}, "params": {"type": "array", "items": {"type": "object", "properties": {"param": {"type": "string"}, "value": {"type": "any"}}}}}}}}}}

                try:
                    validictory.validate(test, conf_schema)
                except Exception as ex:
                    raise ValidationError(str(ex))


'''
# [sep.17] pourquoi se reconnecter au broker à chaque message de device sauvé ???
# because reconnect while already connected implies error with previous connection !!
# moreover, loop_forever manage reconnection ;)
@receiver(post_save, sender=Device)
def on_device_update(sender, **kwargs):
    from devices.tasks.broker import broker_reload
    broker_reload.delay()
'''


#
# [Oct.17] pre_save hook for devices
@receiver(pre_save, sender=Device)
def pre_save_device_callback(sender, instance, **kwargs):
    if( instance.mqtt_defaults == True ):
        # cancel whatever 'server' and 'port' fields may contain
        instance.mqtt_server = None
        instance.mqtt_port = None


@receiver(m2m_changed, sender=Device.locations.through)
def on_locations_update_device(sender, instance, action, model, pk_set, **kwargs):
    if action == "pre_remove":
        for loc in Location.objects.filter(id__in=pk_set):
            perm = Permission.objects.filter(topic=loc.topic + "/+", device=instance, permission_type='PUB')
            perm.delete()

            perm = Permission.objects.filter(topic=loc.topic + "/+/command", device=instance, permission_type='SUB')
            perm.delete()

    if action == "post_add":
        try:
            for loc in Location.objects.filter(id__in=pk_set):
                perm = Permission(topic=loc.topic + "/+", device=instance, permission_type='PUB')
                perm.save()

                perm = Permission(topic=loc.topic + "/+/command", device=instance, permission_type='SUB')
                perm.save()
        except Exception as ex:
            print("Failed to create base permissions for " + str(instance) + ", " + str(ex))


