# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-09-12 19:56
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0026_auto_20160415_1824'),
    ]

    operations = [
        migrations.AddField(
            model_name='check',
            name='nag_time',
            field=models.DurationField(default=datetime.timedelta(0, 60)),
        ),
        migrations.AddField(
            model_name='check',
            name='next_nag_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
