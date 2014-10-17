#file: multimedia/models.py
from django.db import models
from apps.users.models import User


class Position(models.Model):
    DEVICE_TYPE = {
        "Unknown": '??',
        "Android": 'GA',
        "iOs": 'AI',
        "BlackBerry": 'BB',
        "Windows Phone": 'WP',
        "Browser": 'BW',
    }

    DEVICE_TYPES = (
        (DEVICE_TYPE["Unknown"],        "Unknown"),
        (DEVICE_TYPE["Android"],        "Android"),
        (DEVICE_TYPE["iOs"],            "iOs"),
        (DEVICE_TYPE["BlackBerry"],     "BlackBerry"),
        (DEVICE_TYPE["Windows Phone"],  "Windows Phone"),
        (DEVICE_TYPE["Browser"],        "Browser"),
    )

    user = models.ForeignKey(User, related_name='positions')

    #Positional info
    lat     = models.FloatField(default=0)
    lon     = models.FloatField(default=0)
    alt     = models.FloatField(default=0, null=True)
    speed   = models.FloatField(default=0, null=True)
    heading = models.FloatField(default=0, null=True)

    #Aditional data
    accuracy     = models.FloatField(default=0, null=True)
    alt_accuracy = models.FloatField(default=0, null=True)
    timestamp    = models.DateTimeField()
    device_type  = models.CharField(choices=DEVICE_TYPES, max_length=2, default=DEVICE_TYPE["Unknown"])
    app_version  = models.CharField(null=True, max_length=16)
    extra        = models.TextField(null=True, default="")

    #Server data
    _created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-_created_at']

    #@staticmethod
    #def some_static_method(request, arg1):

    def preview(self, user):
        result = {
            "id": self.pk,
            "user_id": self.user.id,
            "lat": self.lat,
            "lon": self.lon,
            "accuracy": self.accuracy,
            "timestamp": self.timestamp.isoformat(),
        }

        return result

    def serialize(self, user):
        result = dict(self.preview(user), **{
            "alt": self.alt,
            "speed": self.speed,
            "heading": self.heading,
            "alt_accuracy": self.alt_accuracy,
            "extra": self.extra,
            "device_type": self.device_type,
            "created_at": self._created_at.isoformat(),
        })

        return result

    def __unicode__(self):
        return "%s at %s" % (self.file.user.name, self.timestamp.isoformat())
