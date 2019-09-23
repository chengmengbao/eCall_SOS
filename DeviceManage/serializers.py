# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2019/9/12 15:29
# @Author  : Paul Chan
# @Email   : paul_chengmengbao@163.com
# @File    : serializers.py
# @Software: PyCharm
from rest_framework import serializers
from .models import Device, SosGps, SosContactPerson


class SosGpsSerializer(serializers.ModelSerializer):
    devicephone = serializers.CharField(source="device.devicephone", read_only=True)
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    update_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    class Meta:
        model = SosGps
        fields = '__all__'


class SosContactPersonSerializer(serializers.ModelSerializer):
    devicephone = serializers.CharField(source="device.devicephone", read_only=True)
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    update_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    class Meta:
        model = SosContactPerson
        fields = '__all__'


class DevicesSerializer(serializers.ModelSerializer):
    sosgps = SosGpsSerializer(many=True, read_only=True)
    soscontactperson = SosContactPersonSerializer(many=True, read_only=True)
    create_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    update_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", required=False, read_only=True)
    class Meta:
        model = Device
        fields = '__all__'