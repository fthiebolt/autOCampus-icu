from django.db import models

from devices.utils import sanitize_string


class Building(models.Model):
    name = models.CharField(max_length=64, blank=False, null=False, unique=True)
    description = models.CharField(max_length=2048)

    topic = models.CharField(max_length=64, editable=False, unique=True)

    def __str__(self):
        return '%s' % self.name

    def clean(self):
        self.topic = sanitize_string(self.name)


class Location(models.Model):
    building = models.ForeignKey(Building, blank=False, null=False)
    room = models.CharField(max_length=64, blank=False, null=False)

    topic = models.CharField(max_length=130, unique=True)

    class Meta:
        unique_together = ('building', 'room')

    def __str__(self):
        return '%s %s' % (self.building.name, self.room)

    def clean(self):
        self.topic = self.building.topic + '/' + sanitize_string(self.room)
