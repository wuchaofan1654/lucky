from utils.serializers import CustomModelSerializer
from custom.models import CheckResult
from rest_framework import serializers


# ================================================= #
# ************** 检查记录管理 序列化器  ************** #
# ================================================= #

class CheckResultSerializer(CustomModelSerializer):
    """
    检查记录管理 简单序列化器
    """
    class Meta:
        model = CheckResult
        exclude = ('description', 'creator', 'modifier')


class CheckResultCreateUpdateSerializer(CustomModelSerializer):
    """
    检查记录管理 创建/更新时的列化器
    """

    def validate(self, attrs: dict):
        return super().validate(attrs)

    class Meta:
        model = CheckResult
        fields = '__all__'
