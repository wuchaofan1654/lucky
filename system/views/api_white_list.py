# -*- coding: utf-8 -*-

"""
@author: wuchaofan
@Created on: 2022/1/1 001 9:34
@Remark:
"""
from system.models import ApiWhiteList
from system.serializers import ApiWhiteListSerializer
from utils.viewset import CustomModelViewSet


class ApiWhiteListViewSet(CustomModelViewSet):
    """
    接口白名单
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = ApiWhiteList.objects.all()
    serializer_class = ApiWhiteListSerializer
    # permission_classes = []
