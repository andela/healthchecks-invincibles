# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-09-14 14:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0027_auto_20170912_1956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='check',
            name='status',
            field=models.CharField(choices=[('up', 'Up'), ('down', 'Down'), ('new', 'New'), ('paused', 'Paused'), ('nag', 'nag')], default='new', max_length=6),
        ),
    ]
