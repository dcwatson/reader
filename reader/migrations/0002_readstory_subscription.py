# encoding: utf8
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        (b'reader', b'0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name=b'ReadStory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'user', models.ForeignKey(to=b'reader.User', to_field='id')),
                (b'story', models.ForeignKey(to=b'reader.Story', to_field='id')),
                (b'is_read', models.BooleanField(default=True)),
                (b'is_starred', models.BooleanField(default=False)),
                (b'notes', models.TextField(blank=True)),
                (b'date_read', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'unique_together': set([(b'user', b'story')]),
                'verbose_name_plural': 'read stories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name=b'Subscription',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (b'user', models.ForeignKey(to=b'reader.User', to_field='id')),
                (b'feed', models.ForeignKey(to=b'reader.Feed', to_field='id')),
                (b'show_read', models.IntegerField(default=7, verbose_name='show read stories back', choices=[(0, b'Do not show read stories'), (1, b'1 day'), (2, b'2 days'), (3, b'3 days'), (4, b'4 days'), (5, b'5 days'), (6, b'6 days'), (7, b'7 days (1 week)'), (14, b'14 days (2 weeks)'), (28, b'28 days (4 weeks)'), (-10, b'10 stories'), (-25, b'25 stories'), (-50, b'50 stories')])),
                (b'date_subscribed', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
                'unique_together': set([(b'user', b'feed')]),
            },
            bases=(models.Model,),
        ),
    ]
