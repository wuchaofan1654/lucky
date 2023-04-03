
from utils.permission import CustomPermission
from utils.filters import DataLevelPermissionsFilter
from utils.viewset import CustomModelViewSet
from custom.filters import RecordingFilter
from custom.models import Recording
from custom.serializers import RecordingSerializer, RecordingCreateUpdateSerializer


class RecordingModelViewSet(CustomModelViewSet):
    """
    录制记录模型 的CRUD视图
    """
    queryset = Recording.objects.all()
    serializer_class = RecordingSerializer
    create_serializer_class = RecordingCreateUpdateSerializer
    update_serializer_class = RecordingCreateUpdateSerializer
    filter_class = RecordingFilter
    extra_filter_backends = [DataLevelPermissionsFilter]
    update_extra_permission_classes = (CustomPermission,)
    destroy_extra_permission_classes = (CustomPermission,)
    create_extra_permission_classes = (CustomPermission,)
    search_fields = ('path', 'host', 'unique_name')
    ordering = 'create_datetime'  # 默认排序
