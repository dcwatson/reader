# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Subscription.show_read'
        db.add_column(u'reader_subscription', 'show_read',
                      self.gf('django.db.models.fields.IntegerField')(default=7),
                      keep_default=False)

        # Adding unique constraint on 'Subscription', fields ['feed', 'user']
        db.create_unique(u'reader_subscription', ['feed_id', 'user_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Subscription', fields ['feed', 'user']
        db.delete_unique(u'reader_subscription', ['feed_id', 'user_id'])

        # Deleting field 'Subscription.show_read'
        db.delete_column(u'reader_subscription', 'show_read')


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
            'Meta': {'unique_together': "(('user', 'story'),)", 'object_name': 'ReadStory'},
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
            'Meta': {'unique_together': "(('user', 'feed'),)", 'object_name': 'Subscription'},
            'date_subscribed': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'feed': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subscriptions'", 'to': u"orm['reader.Feed']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'show_read': ('django.db.models.fields.IntegerField', [], {'default': '7'}),
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