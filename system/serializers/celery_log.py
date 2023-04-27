from system.utils.serializers import CustomModelSerializer
from system.models import CeleryLog


# ================================================= #
# ************** celery定时日志 序列化器  ************** #
# ================================================= #

class CeleryLogSerializer(CustomModelSerializer):
    """
    定时日志 简单序列化器
    """

    class Meta:
        model = CeleryLog
        fields = "__all__"


class ExportCeleryLogSerializer(CustomModelSerializer):
    """
    导出 定时日志 简单序列化器
    """

    class Meta:
        model = CeleryLog
        fields = ('name', 'kwargs', 'seconds', 'status', 'result', 'creator_name')

