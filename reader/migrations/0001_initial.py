# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name=b'User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'password', models.CharField(max_length=128, verbose_name='password')),
                (b'last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                (b'name', models.CharField(max_length=200, blank=True)),
                (b'email', models.EmailField(unique=True, max_length=75, verbose_name='email address')),
                (b'is_admin', models.BooleanField(default=False)),
                (b'is_active', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name=b'Feed',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'url', models.CharField(unique=True, max_length=300)),
                (b'title', models.CharField(max_length=200, blank=True)),
                (b'subtitle', models.TextField(blank=True)),
                (b'status', models.CharField(default=b'new', max_length=20, choices=[(b'new', b'New'), (b'valid', b'Valid'), (b'error', b'Error'), (b'gone', b'Gone')])),
                (b'date_created', models.DateTimeField(default=django.utils.timezone.now)),
                (b'date_updated', models.DateTimeField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name=b'LoginToken',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'user', models.ForeignKey(to=b'reader.User', to_field='id')),
                (b'token', models.CharField(max_length=40)),
                (b'date_created', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'unique_together': set([(b'user', b'token')]),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name=b'SmartFeed',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'user', models.ForeignKey(to=b'reader.User', to_field='id')),
                (b'title', models.CharField(max_length=100, blank=True)),
                (b'query', models.CharField(max_length=100, blank=True)),
                (b'read', models.NullBooleanField()),
                (b'starred', models.NullBooleanField()),
                (b'limit', models.IntegerField(default=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name=b'Story',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'feed', models.ForeignKey(to=b'reader.Feed', to_field='id')),
                (b'ident', models.CharField(unique=True, max_length=40)),
                (b'title', models.CharField(max_length=300)),
                (b'author', models.CharField(max_length=200, blank=True)),
                (b'content', models.TextField(blank=True)),
                (b'link', models.CharField(max_length=300, blank=True)),
                (b'date_published', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name_plural': 'stories',
            },
            bases=(models.Model,),
        ),
    ]
