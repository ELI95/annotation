# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-20 10:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_auto_20180607_1600'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='name',
            field=models.CharField(max_length=128, null=True),
        ),
    ]
