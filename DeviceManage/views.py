# -*- coding: utf-8 -*-
from rest_framework import viewsets
from rest_framework import mixins
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.response import Response

import json

from .models import Device, SosGps, SosContactPerson
from .serializers import DevicesSerializer, SosGpsSerializer, SosContactPersonSerializer
from utils.mqtt_pub_sub import mqtt_client

# Create your views here.
class AllPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100


# 对前端的接口---设备 ---增删改查
class DevicesListViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.all()
    serializer_class = DevicesSerializer
    pagination_class = AllPagination


# 对前端的接口---设备坐标信息 ---只查(需要加/?device=id)
class SosGpsListViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = SosGps.objects.all()
    serializer_class = SosGpsSerializer
    # pagination_class = AllPagination

    # 查
    def list(self, request, *args, **kwargs):
        # queryset = self.filter_queryset(self.get_queryset())
        queryset = SosGps.objects.filter(device=request.query_params.get("device", None))
        # print("queryset:", queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


# 对前端的接口---设备绑定紧急联系人 ---增删改查
# 增：只能增加3个紧急联系人
# 查：(需要加/?device=id)
class SosContactPersonListViewSet(viewsets.ModelViewSet):
    queryset = SosContactPerson.objects.all()

    serializer_class = SosContactPersonSerializer
    pagination_class = AllPagination

    # 查
    def list(self, request, *args, **kwargs):
        # queryset = self.filter_queryset(self.get_queryset())
        queryset = SosContactPerson.objects.filter(device=request.query_params.get("device", None))
        # print("queryset:", queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # 增
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        obj_count = SosContactPerson.objects.filter(device=serializer.validated_data["device"]).count()
        if obj_count < 3:
            self.perform_create(serializer)
        else:
            return Response({"msg": "已超过3个紧急联系人", "code": 40002})

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


# 对终端的接口---接收终端发来的坐标数据
class ReceiveSosView(APIView):
    def post(self, request):
        print("request.data:", request.data, type(request.data))
        devicephone = request.data.get("devicephone", None)
        devicelongitude = request.data.get("devicelongitude", None)
        devicelatitude = request.data.get("devicelatitude", None)
        print("request.data:", devicephone, devicelongitude, devicelatitude)
        if devicephone is not None and devicelongitude is not None and devicelatitude is not None:
            device = Device.objects.filter(devicephone=devicephone).first()
            print("device:", device)
            if device:
                SosGps.objects.create(devicelongitude=devicelongitude, devicelatitude=devicelatitude, device=device)
                return Response({"msg": "成功插入一条数据", "code": 200})
            else:
                return Response({"msg": "该设备未注册在管理系统", "code": 40000})
        else:
            return Response({"msg": "request.data其字段有空值", "code": 40001})


# 对前端的接口---下发紧急联系人到终端
# 查：(需要加/?device=id)
class SendSosContactPersonViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = SosContactPerson.objects.all()
    serializer_class = SosContactPersonSerializer
    # pagination_class = AllPagination

    # 查
    def list(self, request, *args, **kwargs):
        # queryset = self.filter_queryset(self.get_queryset())
        device = request.query_params.get("device", None)
        if device is not None:
            queryset = SosContactPerson.objects.filter(device=device)
            # print("queryset:", queryset)
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)

            contact_info = dict()

            contact_info["pname1"] = serializer.data[0]["personname"]
            contact_info["phone1"] = serializer.data[0]["personphone"]
            contact_info["pname2"] = serializer.data[1]["personname"]
            contact_info["phone2"] = serializer.data[1]["personphone"]
            contact_info["pname3"] = serializer.data[2]["personname"]
            contact_info["phone3"] = serializer.data[2]["personphone"]
            # 测试一下

            device_obj = Device.objects.filter(id=device).first()
            topic_str = "devices/{}/soscontactperson".format(device_obj.devicephone)
            # print("topic_str:", topic_str, type(topic_str))
            msg_str = json.dumps(contact_info)
            # print("msg_str:", msg_str, type(msg_str))

            try:
                # 返回值为None
                mqtt_client.publish_single(topic_str, msg_str, 1)
            except Exception as e:
                return Response({"msg": "下发紧急联系人失败", "code": 40003})

            return Response({"msg": contact_info, "code": 200})
        else:
            return Response({"msg": "没有?device=xxx参数", "code": 40004})
