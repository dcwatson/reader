# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'User'
        db.create_table(u'reader_user', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=75)),
            ('is_admin', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'reader', ['User'])

        # Adding model 'LoginToken'
        db.create_table(u'reader_logintoken', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='login_tokens', to=orm['reader.User'])),
            ('token', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal(u'reader', ['LoginToken'])

        # Adding unique constraint on 'LoginToken', fields ['user', 'token']
        db.create_unique(u'reader_logintoken', ['user_id', 'token'])

        # Adding model 'Feed'
        db.create_table(u'reader_feed', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.CharField')(unique=True, max_length=300)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('subtitle', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='new', max_length=20)),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('date_updated', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'reader', ['Feed'])

        # Adding model 'Story'
        db.create_table(u'reader_story', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('feed', self.gf('django.db.models.fields.related.ForeignKey')(related_name='stories', to=orm['reader.Feed'])),
            ('ident', self.gf('django.db.models.fields.CharField')(unique=True, max_length=40)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('content', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('link', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('date_published', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal(u'reader', ['Story'])

        # Adding model 'Subscription'
        db.create_table(u'reader_subscription', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='subscriptions', to=orm['reader.User'])),
            ('feed', self.gf('django.db.models.fields.related.ForeignKey')(related_name='subscriptions', to=orm['reader.Feed'])),
            ('date_subscribed', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal(u'reader', ['Subscription'])

        # Adding model 'ReadStory'
        db.create_table(u'reader_readstory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='read_stories', to=orm['reader.User'])),
            ('story', self.gf('django.db.models.fields.related.ForeignKey')(related_name='read_stories', to=orm['reader.Story'])),
            ('is_read', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_starred', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('date_read', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal(u'reader', ['ReadStory'])


    def backwards(self, orm):
        # Removing unique constraint on 'LoginToken', fields ['user', 'token']
        db.delete_unique(u'reader_logintoken', ['user_id', 'token'])

        # Deleting model 'User'
        db.delete_table(u'reader_user')

        # Deleting model 'LoginToken'
        db.delete_table(u'reader_logintoken')

        # Deleting model 'Feed'
        db.delete_table(u'reader_feed')

        # Deleting model 'Story'
        db.delete_table(u'reader_story')

        # Deleting model 'Subscription'
        db.delete_table(u'reader_subscription')

        # Deleting model 'ReadStory'
        db.delete_table(u'reader_readstory')


    models = {
        u'reader.feed': {
            'Meta': {'object_name': 'Feed'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date_updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '20'}),
            'subtitle': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '300'})
        },
        u'reader.logintoken': {
            'Meta': {'unique_together': "(('user', 'token'),)", 'object_name': 'LoginToken'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'login_tokens'", 'to': u"orm['reader.User']"})
        },
        u'reader.readstory': {
            'Meta': {'object_name': 'ReadStory'},
            'date_read': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_read': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_starred': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'story': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'read_stories'", 'to': u"orm['reader.Story']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'read_stories'", 'to': u"orm['reader.User']"})
        },
        u'reader.story': {
            'Meta': {'object_name': 'Story'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date_published': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'feed': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stories'", 'to': u"orm['reader.Feed']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ident': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'reader.subscription': {
            'Meta': {'object_name': 'Subscription'},
            'date_subscribed': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'feed': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subscriptions'", 'to': u"orm['reader.Feed']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subscriptions'", 'to': u"orm['reader.User']"})
        },
        u'reader.user': {
            'Meta': {'object_name': 'User'},
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }

    complete_apps = ['reader']