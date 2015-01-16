#import json
from time import mktime

from django.db import models
from django.db import IntegrityError

from apps.users.models import User


class ReferrerProfile(models.Model):
    """ Represents the referrer profile of an user,
        which holds all the referred from the user
    """
    user = models.OneToOneField(User, related_name='referrer_profile')
    token = models.CharField(max_length=8)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('created_at',)

    def refer_user(self, user, client_IP):
        referred = Referred(
            user=user,
            referrer=self,
            IP=client_IP
        )
        try:
            referred.save()
        except IntegrityError:
            return None
        else:
            return referred

    def preview(self, user):
        return {
            'id': self.id,
            'user': self.user.preview(user),
            'token': self.token,
        }

    def serialize(self, user):
        return dict(self.preview(user), **{
            'active': self.active,
            'created_at': int(mktime(self.created_at.timetuple()) * 1000),
        })

    def __unicode__(self):
        return "R(%s)" % (self.user.name)


class Referred(models.Model):
    """A Referred user by a Referrer user."""
    referrer = models.ForeignKey(ReferrerProfile, related_name='referrals')
    user = models.ForeignKey(User, related_name='referrer')
    IP = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)

    class Meta:
        ordering = ('created_at', 'referrer',)
        unique_together = ('user', 'referrer')

    def __unicode__(self):
        return "%s by %s" % (self.user.name, self.referrer,)

    def preview(self, user):
        return {
            'id': self.id,
            'user': self.user.preview(user),
            'accepted': self.accepted,
        }

    def serialize(self, user):
        return dict(self.preview(user), **{
            'referrer': self.referrer.preview(user),
            'created_at': int(mktime(self.created_at.timetuple()) * 1000),
        })
