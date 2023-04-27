# -*- coding: utf-8 -*-

"""
@author: lucky
@contact: QQ:382503189
@Created on: 2022/6/3 003 0:30
@Remark: 按钮权限管理
"""
from system.models import LoginLog
from system.serializers import LoginLogSerializer
from system.utils.viewset import CustomModelViewSet


class LoginLogViewSet(CustomModelViewSet):
    """
    登录日志接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = LoginLog.objects.all()
    serializer_class = LoginLogSerializer
    extra_filter_backends = []
    ordering_fields = ['create_datetime']
