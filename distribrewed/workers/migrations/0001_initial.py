# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-01 22:57
from __future__ import unicode_literals

import django.contrib.postgres.fields
import django.contrib.postgres.fields.hstore
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('id', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=100, null=True)),
                ('inheritance_chain', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), size=None)),
                ('ip_address', models.GenericIPAddressField(null=True, protocol='IPv4')),
                ('prometheus_scrape_port', models.IntegerField(null=True)),
                ('last_registered', models.DateTimeField()),
                ('last_answered_ping', models.DateTimeField(null=True)),
                ('is_answering_ping', models.BooleanField(default=False)),
                ('info', django.contrib.postgres.fields.hstore.HStoreField()),
            ],
        ),
        migrations.CreateModel(
            name='WorkerMethod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('parameters', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=30), size=None)),
                ('worker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workers.Worker')),
            ],
        ),
    ]
