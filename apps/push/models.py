#import json
from time import mktime

from django.db import models
from django.core.exceptions import FieldError

from python_push.gcm.gcm_push_service import GCMPushService
from python_push.blackberry.bb_push_service import BBPushService

from apps.users.models import User


class Device(models.Model):
    """A mobile Device"""
    TYPES = (
        (GCMPushService.type, 'Google Android'),
        (BBPushService.type, 'BlackBerry OS'),
        ('AI', 'Apple iOs'),
        ('WP', 'Windows Phone 7'),
        ('WB', 'Web Browser'),
        ('IO', 'Socket.IO'),
    )

    user = models.ForeignKey(User, related_name='devices')
    token = models.CharField(max_length=256)
    type = models.CharField(max_length=2, choices=TYPES)
    last_sync = models.DateTimeField(auto_now_add=True, auto_now=True)

    class Meta:
        unique_together = ('token', 'type')

    def save(self, *args, **kwargs):
        if self.type not in map(lambda t: t[0], Device.TYPES):
            raise FieldError('Invalid value of Device.type')
        super(Device, self).save(*args, **kwargs)

    def preview(self, user):
        return {
            'id': self.id,
            'type': self.type,
        }

    def serialize(self, user):
        return self.preview(user)


class Chunk(models.Model):
    """A chunk of data waiting to be sync"""
    data = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    expiration = models.DateTimeField()
    devices = models.ManyToManyField(Device, related_name='chunks')
    devices_number = models.IntegerField(default=0)

    class Meta:
        ordering = ['created_at']

    def add_device(self, device, save=True):
        self.devices.add(device)
        self.devices_number = self.devices.count()

        if save:
            self.save()

    def add_devices(self, devices):
        for device in devices:
            self.add_device(device, False)
        self.save()

    def remove_device(self, device, save=True):
        self.devices.remove(device)
        self.devices_number = self.devices.count()

        if self.devices_number < 1:
            self.delete()
        elif save:
            self.save()

    def preview(self, user):
        return {
            'data': self.data
        }

    def serialize(self, user):
        return dict(self.preview(user),
            **{
                'id': self.id,
                'created_at': int(mktime(self.created_at.timetuple()) * 1000),
                'expiration': int(mktime(self.expiration.timetuple()) * 1000),
                'devices': map(lambda d: d.preview(user), self.devices.all()[:10]),
                'devices_number': self.devices_number,
            })
