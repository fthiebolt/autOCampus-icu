from django.db import models
from django.contrib import admin
from django.core.exceptions import ValidationError, FieldError

from devices.utils import sanitize_string


class Permission(models.Model):
    topic = models.CharField(max_length=2048)

    device = models.ForeignKey('Device', on_delete=models.CASCADE)

    perm_type_choices = (
        ('PUB', 'Publish'),
        ('SUB', 'Subscribe'),
        ('ALL', 'Publish/Subscribe'),
    )

    permission_type = models.CharField(max_length=3, choices=perm_type_choices, default='ALL')

    def __str__(self):
        return '%s' % self.topic

    def match_type(self, t):
        return (t == 'PUB' and (self.permission_type == 'PUB' or self.permission_type == 'ALL')) or\
               (t == 'SUB' and (self.permission_type == 'SUB' or self.permission_type == 'ALL'))


class PermissionInline(admin.TabularInline):
    model = Permission
