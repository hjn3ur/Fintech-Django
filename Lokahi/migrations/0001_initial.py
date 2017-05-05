# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('company_time', models.DateTimeField(blank=True, null=True, default=datetime.datetime.now)),
                ('company_update', models.DateTimeField(blank=True, null=True, default=datetime.datetime.now)),
                ('company_name', models.CharField(max_length=50)),
                ('company_username', models.CharField(max_length=30, default='')),
                ('company_password', models.CharField(max_length=30, default='')),
                ('company_ceo', models.CharField(max_length=50, default='')),
                ('company_email', models.EmailField(max_length=254, default='')),
                ('company_state', models.CharField(max_length=20, default='')),
                ('company_country', models.CharField(max_length=20, default='')),
                ('company_phone', models.CharField(max_length=20, default='')),
                ('company_sector', models.CharField(max_length=50, default='')),
                ('company_industry', models.CharField(max_length=50, default='')),
                ('company_project', models.TextField(max_length=1000, default='')),
                ('banned', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Investor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('username', models.CharField(max_length=30, default='')),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=30, default='')),
                ('banned', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('message_timestamp', models.DateTimeField(blank=True, null=True, default=datetime.datetime.now)),
                ('receiver', models.CharField(max_length=30, default='')),
                ('sender', models.CharField(max_length=30, default='')),
                ('message', models.CharField(max_length=1000, null=True, default='')),
                ('encrypted_message', models.BinaryField(max_length=5000, null=True)),
                ('encrypted', models.NullBooleanField(default=False)),
                ('RSA_key', models.CharField(max_length=1000, blank=True, null=True, default='')),
                ('hash_id', models.CharField(max_length=25, blank=True, null=True, default='')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('read', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('files_id', models.CharField(max_length=50, default='')),
                ('picfile', models.FileField(upload_to='pictures')),
                ('timestamp', models.DateTimeField(blank=True, null=True, default=datetime.datetime.now)),
                ('owner', models.CharField(max_length=50, default='')),
                ('investor', models.CharField(max_length=50, default='')),
                ('encrypted', models.NullBooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('project_id', models.CharField(max_length=50, default='')),
                ('timestamp', models.DateTimeField(blank=True, null=True, default=datetime.datetime.now)),
                ('owner', models.CharField(max_length=50, default='')),
                ('project', models.CharField(max_length=50, default='')),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('report_id', models.AutoField(primary_key=True, serialize=False)),
                ('public', models.CharField(max_length=50, default='')),
                ('private', models.CharField(max_length=50, default='')),
                ('company_time', models.DateTimeField(blank=True, null=True, default=datetime.datetime.now)),
                ('company_update', models.DateTimeField(blank=True, null=True, default=datetime.datetime.now)),
                ('company_name', models.CharField(max_length=50, default='')),
                ('company_ceo', models.CharField(max_length=50, default='')),
                ('company_email', models.EmailField(max_length=254, default='')),
                ('company_phone', models.CharField(max_length=20, default='')),
                ('company_state', models.CharField(max_length=20, default='')),
                ('company_country', models.CharField(max_length=20, default='')),
                ('company_sector', models.CharField(max_length=50, default='')),
                ('company_industry', models.CharField(max_length=50, default='')),
                ('company_project', models.TextField(max_length=1000, default='')),
                ('company_file', models.TextField(max_length=1000, null=True)),
                ('company_groups', models.CharField(max_length=1000, default='')),
            ],
        ),
    ]
