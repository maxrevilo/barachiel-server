# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Permission'
        db.create_table(u'auth_permission', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('codename', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'auth', ['Permission'])

        # Adding unique constraint on 'Permission', fields ['content_type', 'codename']
        db.create_unique(u'auth_permission', ['content_type_id', 'codename'])

        # Adding model 'Group'
        db.create_table(u'auth_group', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=80)),
        ))
        db.send_create_signal(u'auth', ['Group'])

        # Adding M2M table for field permissions on 'Group'
        m2m_table_name = db.shorten_name(u'auth_group_permissions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('group', models.ForeignKey(orm[u'auth.group'], null=False)),
            ('permission', models.ForeignKey(orm[u'auth.permission'], null=False))
        ))
        db.create_unique(m2m_table_name, ['group_id', 'permission_id'])

        # Adding model 'Confirmation'
        db.create_table(u'auth_confirmation', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='confirmations', to=orm['users.User'])),
            ('token', self.gf('django.db.models.fields.CharField')(unique=True, max_length=8)),
            ('confirmation_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'auth', ['Confirmation'])


    def backwards(self, orm):
        # Removing unique constraint on 'Permission', fields ['content_type', 'codename']
        db.delete_unique(u'auth_permission', ['content_type_id', 'codename'])

        # Deleting model 'Permission'
        db.delete_table(u'auth_permission')

        # Deleting model 'Group'
        db.delete_table(u'auth_group')

        # Removing M2M table for field permissions on 'Group'
        db.delete_table(db.shorten_name(u'auth_group_permissions'))

        # Deleting model 'Confirmation'
        db.delete_table(u'auth_confirmation')


    models = {
        u'auth.confirmation': {
            'Meta': {'object_name': 'Confirmation'},
            'confirmation_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'token': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '8'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'confirmations'", 'to': u"orm['users.User']"})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
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

    complete_apps = ['auth']