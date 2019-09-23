# -*- coding: utf-8 -*-

from django.db import models

'''
数据库的表创建和更改的迁移
python3 manage.py makemigrations remote_upgrade_app01
python3 manage.py migrate
'''


# Create your models here.
class Device(models.Model):
    """
    终端信息表
    """
    # FLAG_CHOICES = (
    #     (0, 'normal'),
    #     (1, 'sos')
    # )
    deviceid = models.CharField(max_length=8, unique=True, default="", verbose_name="终端ID")
    devicephone = models.CharField(max_length=11, unique=True, default="", verbose_name="终端手机号")

    # deviceflag = models.SmallIntegerField(choices=FLAG_CHOICES, default=0, verbose_name="是否告警")

    # 具有auto_now_add属性，创建记录时会自动填充当前时间到此字段
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    # 具有auto_now属性，当记录发生变化时填充当前时间到此字段，注意：用update（）方法更新时不会自动更新当前时间这个字段
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = "终端信息"
        verbose_name_plural = verbose_name
        ordering = ('-create_time',)

    def __str__(self):
        return self.devicephone


class SosGps(models.Model):
    """
    终端gps坐标信息表
    """
    devicelongitude = models.CharField(max_length=30, null=True, blank=True, verbose_name="终端GPS的经度")
    devicelatitude = models.CharField(max_length=30, null=True, blank=True, verbose_name="终端GPS的纬度")
    device = models.ForeignKey(Device, related_name="sosgps", verbose_name="绑定终端")
    # 具有auto_now_add属性，创建记录时会自动填充当前时间到此字段
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    # 具有auto_now属性，当记录发生变化时填充当前时间到此字段，注意：用update（）方法更新时不会自动更新当前时间这个字段
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = "终端gps坐标信息"
        verbose_name_plural = verbose_name
        ordering = ('-create_time',)

    def __str__(self):
        return self.device.devicephone


class SosContactPerson(models.Model):
    """
    紧急联系人表
    """
    personname = models.CharField(max_length=30, default="", verbose_name="紧急联系人名字")
    personphone = models.CharField(max_length=11, unique=True, default="", verbose_name="紧急联系人手机号")
    # 具有auto_now_add属性，创建记录时会自动填充当前时间到此字段
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    # 具有auto_now属性，当记录发生变化时填充当前时间到此字段，注意：用update（）方法更新时不会自动更新当前时间这个字段
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    device = models.ForeignKey(Device, related_name="soscontactperson", verbose_name="绑定终端")

    class Meta:
        verbose_name = "紧急联系人信息"
        verbose_name_plural = verbose_name
        ordering = ('create_time',)

    def __str__(self):
        return self.personname