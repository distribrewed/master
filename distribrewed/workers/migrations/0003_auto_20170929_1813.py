# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-29 18:13
from __future__ import unicode_literals

import django.contrib.postgres.fields
import django.contrib.postgres.fields.hstore
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workers', '0002_workermethod'),
    ]

    operations = [
        migrations.AddField(
            model_name='worker',
            name='info',
            field=django.contrib.postgres.fields.hstore.HStoreField(default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='worker',
            name='inheritance_chain',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), default=None, size=None),
            preserve_default=False,
        ),
    ]
