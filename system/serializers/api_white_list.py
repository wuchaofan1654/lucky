
from system.models import ApiWhiteList
from utils.serializers import CustomModelSerializer


class ApiWhiteListSerializer(CustomModelSerializer):
    """
    接口白名单-序列化器
    """

    class Meta:
        model = ApiWhiteList
        fields = "__all__"
        read_only_fields = ["id"]


class ApiWhiteListInitSerializer(CustomModelSerializer):
    """
    初始化获取数信息(用于生成初始化json文件)
    """

    class Meta:
        model = ApiWhiteList
        fields = ['url', 'method', 'enable_datasource', 'creator', 'dept_belong_id']
        read_only_fields = ["id"]
        extra_kwargs = {
            'creator': {'write_only': True},
            'dept_belong_id': {'write_only': True}
        }

