# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-20 11:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_project_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(default='unnamed project', max_length=128),
        ),
    ]
