#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
#from yougrups import settings
from apps.users.models import User


class Like(models.Model):

    liker     = models.ForeignKey(User, related_name='likes_from')
    liked     = models.ForeignKey(User, related_name='likes_to')
    anonymous = models.BooleanField(default=False)
    geo_lat   = models.FloatField(default=0)
    geo_lon   = models.FloatField(default=0)

    #Server data
    _updated_at = models.DateTimeField(auto_now=True, auto_now_add=True)
    _created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.geo_lat = self.liker.geo_lat
        self.geo_lon = self.liker.geo_lon

        super(Like, self).save(*args, **kwargs)

        self.recalculate_likes()

    def delete(self, *args, **kwargs):
        super(Like, self).delete(*args, **kwargs)
        self.recalculate_likes()

    def recalculate_likes(self):
        self.liker.likes_number = self.liker.likes_from.count()
        self.liker.save()
        self.liked.liked_number = self.liked.likes_to.count()
        self.liked.save()

    def preview(self, user):
        result = None

        if user == self.liker or user == self.liked:
            result = {
                'id': self.id,
                'user': None,
                'liked': user == self.liker,
                '_updated_at': self._updated_at.isoformat(),
                'anonymous': self.anonymous
            }

            if user == self.liker:
                result['user'] = self.liked.preview(user)
            elif self.anonymous:
                result['user'] = self.liker.preview_anonym(user)
            else:
                result['user'] = self.liker.preview(user)

        return result

    def serialize(self, user):
        result = None

        if user == self.liker or user == self.liked:
            result = dict(self.preview(user),
                **{
                    '_created_at': self._created_at.isoformat(),
                    'messages': map(lambda l: l.preview(user), self.messages.all()[:100])
                })

            if user == self.liker or not self.anonymous:
                result['geo_lat'] = str(self.geo_lat)
                result['geo_lon'] = str(self.geo_lon)

        return result

    def __unicode__(self):
        return "%s To %s" % (self.liker, self.liked)

    class Meta:
        unique_together = ('liker', 'liked')
        ordering = ['_updated_at']


class LikeMessage(models.Model):
    author  = models.ForeignKey(User, related_name='messages')
    like    = models.ForeignKey(Like, related_name='messages')
    content = models.TextField(blank=True, default=None, null=True)
    geo_lat = models.FloatField(default=0)
    geo_lon = models.FloatField(default=0)
    # Remove when enough time
    extra = models.TextField(blank=True, default=None, null=True)

    #Server data
    _updated_at = models.DateTimeField(auto_now=True, auto_now_add=True)
    _created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.geo_lat = self.author.geo_lat
        self.geo_lon = self.author.geo_lon

        super(Like, self).save(*args, **kwargs)

    def preview(self, user):
        result = None

        if user == self.like.liker or user == self.like.liked:
            result = {
                'yours': self.author == user,
                'content': self.content,
                '_created_at': self._created_at.isoformat(),
            }

        return result

    def serialize(self, user):
        result = None

        if user == self.like.liker or user == self.like.liked:
            result = dict(self.preview(user),
                **{
                    'id': self.id,
                })

            # if user == self.like.liker or not self.like.anonymous:
            #     result['geo_lat'] = str(self.geo_lat)
            #     result['geo_lon'] = str(self.geo_lon)

        return result

    def __unicode__(self):
        return "%s at %s" % (self.author, self._created_at.isoformat())
