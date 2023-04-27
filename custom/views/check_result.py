
from system.utils.viewset import CustomModelViewSet
from custom.models import CheckResult
from custom.serializers import CheckResultSerializer, CheckResultCreateUpdateSerializer


class CheckResultModelViewSet(CustomModelViewSet):
    """
    检查结果模型 的CRUD视图
    """
    queryset = CheckResult.objects.all()
    serializer_class = CheckResultSerializer
    create_serializer_class = CheckResultCreateUpdateSerializer
    update_serializer_class = CheckResultCreateUpdateSerializer

    # 导出
    # export_field_label = fields = {
    #     "host": "请求域名",
    #     "path": "请求路径",
    #     "unique_name": "唯一标识名称",
    #     "request_meta": "请求参数",
    #     "response_meta": "响应信息",
    #     "create_datetime": "创建时间"
    # }
    # export_serializer_class = ExportRecordingProfileSerializer
