from system.utils import serializers
from system.utils.serializers import CustomModelSerializer
from custom.models import Recording


# ================================================= #
# ************** 录制记录管理 序列化器  ************** #
# ================================================= #

class RecordingSerializer(CustomModelSerializer):
    """
    录制记录管理 简单序列化器
    """
    class Meta:
        model = Recording
        exclude = ('description', 'creator', 'modifier')


class RecordingCreateUpdateSerializer(CustomModelSerializer):
    """
    录制记录管理 创建/更新时的列化器
    """

    def validate(self, attrs: dict):
        return super().validate(attrs)

    class Meta:
        model = Recording
        fields = '__all__'


class ExportRecordingProfileSerializer(CustomModelSerializer):
    """
    录制记录导出 序列化器
    """

    class Meta:
        model = Recording
        fields = (
            "host",
            "path",
            "unique_name",
            "request_meta",
            "response_meta",
            "create_datetime"
        )

