# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Media'
        db.create_table(u'multimedia_media', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uploader', self.gf('django.db.models.fields.related.ForeignKey')(related_name='uploads', to=orm['users.User'])),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('type', self.gf('django.db.models.fields.CharField')(default='I', max_length=1)),
            ('_created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'multimedia', ['Media'])


    def backwards(self, orm):
        # Deleting model 'Media'
        db.delete_table(u'multimedia_media')


    models = {
        u'likes.like': {
            'Meta': {'ordering': "['_created_at']", 'unique_together': "(('liker', 'liked'),)", 'object_name': 'Like'},
            '_created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            '_updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'anonymous': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'geo_lat': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'geo_lon': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'liked': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'likes_to'", 'to': u"orm['users.User']"}),
            'liker': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'likes_from'", 'to': u"orm['users.User']"})
        },
        u'multimedia.media': {
            'Meta': {'ordering': "['-_created_at']", 'object_name': 'Media'},
            '_created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'I'", 'max_length': '1'}),
            'uploader': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'uploads'", 'to': u"orm['users.User']"})
        },
        u'users.user': {
            'Meta': {'object_name': 'User'},
            '_created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            '_email_wtc': ('django.db.models.fields.EmailField', [], {'default': 'None', 'max_length': '75', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            '_updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'age': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'bio': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'birthday': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'geo_lat': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'geo_lon': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'geo_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'how_can_see_age': ('django.db.models.fields.CharField', [], {'default': "'E'", 'max_length': '1'}),
            'how_can_see_bio': ('django.db.models.fields.CharField', [], {'default': "'E'", 'max_length': '1'}),
            'how_can_see_email': ('django.db.models.fields.CharField', [], {'default': "'L'", 'max_length': '1'}),
            'how_can_see_name': ('django.db.models.fields.CharField', [], {'default': "'E'", 'max_length': '1'}),
            'how_can_see_picture': ('django.db.models.fields.CharField', [], {'default': "'E'", 'max_length': '1'}),
            'how_can_see_ss': ('django.db.models.fields.CharField', [], {'default': "'E'", 'max_length': '1'}),
            'how_can_see_tel': ('django.db.models.fields.CharField', [], {'default': "'L'", 'max_length': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'liked_number': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'likes': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'liked'", 'symmetrical': 'False', 'through': u"orm['likes.Like']", 'to': u"orm['users.User']"}),
            'likes_number': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'off_radar': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'picture': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'user'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['multimedia.Media']"}),
            'r_interest': ('django.db.models.fields.CharField', [], {'default': "'U'", 'max_length': '1'}),
            'sentimental_status': ('django.db.models.fields.CharField', [], {'default': "'U'", 'max_length': '1'}),
            'sex': ('django.db.models.fields.CharField', [], {'default': "'U'", 'max_length': '1'}),
            'tel': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32', 'blank': 'True'})
        }
    }

    complete_apps = ['multimedia']