#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
#from yougrups import settings
from apps.users.models import User
from django.db.models import Q


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

    def add_message(self, message):
        message = LikeMessage(
            author=self.liker,
            like=self,
            content=message,
        )
        message.save()
        return message

    def conversation(self):
        messages = LikeMessage.objects.filter(
            Q(like__liker=self.liker, like__liked=self.liked) |
            Q(like__liker=self.liked, like__liked=self.liker)
        ).order_by('_created_at')

        return messages

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
                'anonymous': self.anonymous,
                '_updated_at': self._updated_at.isoformat()
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
            message_query = self.messages.order_by('-_created_at').all()[:1]
            message = message_query[0].preview(user) if len(message_query) > 0 else None

            result = dict(self.preview(user),
                **{
                    'message': message,
                    'messages': map(lambda l: l.preview(user), self.conversation().all()[:100]),
                    '_created_at': self._created_at.isoformat()
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
        self.content = self.content[:140]

        super(LikeMessage, self).save(*args, **kwargs)

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

    class Meta:
        ordering = ['-_created_at']
