# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-10-12 06:08
from __future__ import unicode_literals

import app_profile.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_profile', '0003_auto_20171009_2031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='photo',
            field=models.ImageField(blank=True, default='img/profile_pic.svg', null=True, upload_to=app_profile.models.user_directory_img_path),
        ),
    ]
