# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-09-16 02:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('DeviceManage', '0006_auto_20190916_1029'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='device',
            name='devicemac',
        ),
    ]