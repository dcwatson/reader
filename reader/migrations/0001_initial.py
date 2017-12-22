# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feed',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('url', models.CharField(max_length=300, unique=True)),
                ('title', models.CharField(max_length=200, blank=True)),
                ('subtitle', models.TextField(blank=True)),
                ('status', models.CharField(default='new', max_length=20, choices=[('new', 'New'), ('valid', 'Valid'), ('error', 'Error'), ('gone', 'Gone')])),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LoginToken',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('token', models.CharField(max_length=40)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(to='users.User', related_name='login_tokens')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ReadStory',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('is_read', models.BooleanField(default=True)),
                ('is_starred', models.BooleanField(default=False)),
                ('notes', models.TextField(blank=True)),
                ('date_read', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name_plural': 'read stories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SmartFeed',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('title', models.CharField(max_length=100, blank=True)),
                ('query', models.CharField(max_length=100, blank=True)),
                ('read', models.NullBooleanField()),
                ('starred', models.NullBooleanField()),
                ('limit', models.IntegerField(default=50)),
                ('user', models.ForeignKey(to='users.User', related_name='smart_feeds')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('ident', models.CharField(max_length=40, unique=True)),
                ('title', models.CharField(max_length=300)),
                ('author', models.CharField(max_length=200, blank=True)),
                ('content', models.TextField(blank=True)),
                ('link', models.CharField(max_length=300, blank=True)),
                ('date_published', models.DateTimeField(default=django.utils.timezone.now)),
                ('feed', models.ForeignKey(to='reader.Feed', related_name='stories')),
            ],
            options={
                'verbose_name_plural': 'stories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('show_read', models.IntegerField(default=7, verbose_name='show read stories back', choices=[(0, 'Do not show read stories'), (1, '1 day'), (2, '2 days'), (3, '3 days'), (4, '4 days'), (5, '5 days'), (6, '6 days'), (7, '7 days (1 week)'), (14, '14 days (2 weeks)'), (28, '28 days (4 weeks)'), (-10, '10 stories'), (-25, '25 stories'), (-50, '50 stories')])),
                ('date_subscribed', models.DateTimeField(default=django.utils.timezone.now)),
                ('feed', models.ForeignKey(to='reader.Feed', related_name='subscriptions')),
                ('user', models.ForeignKey(to='users.User', related_name='subscriptions')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='subscription',
            unique_together=set([('user', 'feed')]),
        ),
        migrations.AddField(
            model_name='readstory',
            name='story',
            field=models.ForeignKey(to='reader.Story', related_name='read_stories'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='readstory',
            name='user',
            field=models.ForeignKey(to='users.User', related_name='read_stories'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='readstory',
            unique_together=set([('user', 'story')]),
        ),
        migrations.AlterUniqueTogether(
            name='logintoken',
            unique_together=set([('user', 'token')]),
        ),
    ]
