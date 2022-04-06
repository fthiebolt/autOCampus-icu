from django.db import models
from django.contrib import admin

from devices.models.device import Device


class LogMessage(models.Model):
    device = models.ForeignKey(Device)

    date = models.DateTimeField()
    remote_ip = models.CharField(max_length=40)
    remote_host = models.CharField(max_length=255)

    levelno = models.IntegerField()
    levelname = models.CharField(max_length=255)

    name = models.CharField(max_length=255)
    module = models.CharField(max_length=255)
    filename = models.CharField(max_length=255)
    pathname = models.CharField(max_length=255)
    funcName = models.CharField(max_length=255)
    lineno = models.IntegerField()

    msg = models.TextField()
    exc_info = models.TextField(null=True, blank=True)
    exc_text = models.TextField(null=True, blank=True)
    args = models.TextField(null=True, blank=True)

    threadName = models.CharField(max_length=255)
    thread = models.FloatField()
    created = models.FloatField()
    process = models.IntegerField()
    relativeCreated = models.FloatField()
    msecs = models.FloatField()

    def formattable_dict(self):
        from django.forms.models import model_to_dict
        import time

        dict = model_to_dict(self)

        dict['asctime'] = str(self.date)
        dict['created'] = str(self.date.time())
        dict['message'] = dict['msg']

        return dict


class LogMessageInline(admin.TabularInline):
    model = LogMessage
    fields = ('device', 'remote_ip', 'date', 'levelname', 'msg')
    readonly_fields = ('device', 'date', 'remote_ip', 'remote_host', 'levelno', 'levelname', 'name', 'module',
                       'filename', 'pathname', 'funcName', 'lineno', 'msg', 'exc_info', 'exc_text', 'args',
                       'threadName', 'thread', 'created', 'process', 'relativeCreated', 'msecs')
    can_delete = False


class LogMessageAdmin(admin.ModelAdmin):
    list_display = ('device', 'remote_ip', 'date', 'levelname', 'msg')

    search_fields = ('device__mac', 'remote_ip', 'date', 'levelname')

    readonly_fields = ('device', 'date', 'remote_ip', 'remote_host', 'levelno', 'levelname', 'name', 'module',
                       'filename', 'pathname', 'funcName', 'lineno', 'msg', 'exc_info', 'exc_text', 'args',
                       'threadName', 'thread', 'created', 'process', 'relativeCreated', 'msecs')
    extra = 0

    def has_add_permission(self, request):
        return False
