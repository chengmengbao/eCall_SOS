# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-09-16 02:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DeviceManage', '0005_auto_20190916_1053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='deviceid',
            field=models.CharField(default='', max_length=8, unique=True, verbose_name='终端ID'),
        ),
    ]