# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-03 17:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0007_auto_20180620_1103'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='tag',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='verify_status',
            field=models.CharField(choices=[('unreleased', '未发布'), ('verifying', '审核中'), ('verification succeed', '审核通过'), ('verification failed', '审核未通过')], default='unreleased', max_length=255),
        ),
    ]
