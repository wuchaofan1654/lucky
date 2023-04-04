# -*- coding: utf-8 -*-

"""
@author: 李强
@contact: QQ:1206709430
@Created on: 2021/6/8 003 0:30
@Remark: 操作日志管理
"""

from system.models import OperationLog
from utils.serializers import CustomModelSerializer


class OperationLogSerializer(CustomModelSerializer):
    """
    日志-序列化器
    """

    class Meta:
        model = OperationLog
        fields = "__all__"
        read_only_fields = ["id"]


class OperationLogCreateUpdateSerializer(CustomModelSerializer):
    """
    操作日志  创建/更新时的列化器
    """

    class Meta:
        model = OperationLog
        fields = '__all__'
