# -*- coding: utf-8 -*-

from system.models import Area
from system.serializers import AreaSerializer
from system.utils.viewset import CustomModelViewSet


class AreaViewSet(CustomModelViewSet):
    """
    地区管理接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    extra_filter_backends = []
