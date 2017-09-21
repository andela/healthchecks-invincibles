# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-20 09:59
from __future__ import unicode_literals

from django.db import migrations, models
import embed_video.fields


class Migration(migrations.Migration):

    dependencies = [
        ('front', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=800)),
                ('video', embed_video.fields.EmbedVideoField()),
            ],
        ),
    ]
