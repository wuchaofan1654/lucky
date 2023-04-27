
# -*- coding: utf-8 -*-

from system.models import CeleryLog
from system.serializers import CeleryLogSerializer
from system.utils.viewset import CustomModelViewSet
from system.utils.json_response import SuccessResponse


class CeleryLogViewSet(CustomModelViewSet):
    """
    celery日志管理接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = CeleryLog.objects.all()
    serializer_class = CeleryLogSerializer
    extra_filter_backends = []

    def clean_all(self, request, *args, **kwargs):
        """
        清空定时任务日志
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        self.get_queryset().delete()
        return SuccessResponse(msg="清空成功")
