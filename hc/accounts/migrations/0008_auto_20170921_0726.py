# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-09-21 07:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20170914_0652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='reports_allowed_daily',
            field=models.BooleanField(default=False),
        ),
    ]
