# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-01 22:57
from __future__ import unicode_literals

import django.contrib.postgres.fields
import django.contrib.postgres.fields.hstore
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, null=True)),
                ('ruleId', models.IntegerField(null=True)),
                ('ruleName', models.CharField(max_length=200, null=True)),
                ('ruleUrl', models.CharField(max_length=200, null=True)),
                ('state', models.CharField(max_length=10, null=True)),
                ('imageUrl', models.CharField(max_length=200, null=True)),
                ('message', models.CharField(max_length=300, null=True)),
                ('evalMatches', django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.hstore.HStoreField(), null=True, size=None)),
            ],
        ),
    ]
