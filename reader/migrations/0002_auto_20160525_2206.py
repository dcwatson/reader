# -*- coding: utf-8 -*-
# Generated by Django 1.10a1 on 2016-05-26 02:06
from __future__ import unicode_literals

from django.db import migrations
import django.contrib.postgres.search


class Migration(migrations.Migration):

    dependencies = [
        ('reader', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='search',
            field=django.contrib.postgres.search.SearchVectorField(null=True),
        ),
    ]
