# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-09-16 02:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DeviceManage', '0003_auto_20190912_1624'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='deviceid',
            field=models.CharField(blank=True, max_length=11, null=True, verbose_name='终端ID'),
        ),
    ]