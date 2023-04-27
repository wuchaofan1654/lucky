import os

from application.settings import BASE_DIR
from system.utils.json_response import SuccessResponse
from system.utils.viewset import CustomModelViewSet
from custom.models import Recording
from custom.serializers import RecordingSerializer, RecordingCreateUpdateSerializer, ExportRecordingProfileSerializer

from system.tasks import websocket_push


class RecordingModelViewSet(CustomModelViewSet):
    """
    录制记录模型 的CRUD视图
    """
    queryset = Recording.objects.all()
    serializer_class = RecordingSerializer
    create_serializer_class = RecordingCreateUpdateSerializer
    update_serializer_class = RecordingCreateUpdateSerializer

    # 导出
    export_field_label = fields = {
        "host": "请求域名",
        "path": "请求路径",
        "unique_name": "唯一标识名称",
        "request_meta": "请求参数",
        "response_meta": "响应信息",
        "create_datetime": "创建时间"
    }
    export_serializer_class = ExportRecordingProfileSerializer

    def receive_push_recording(self):
        # TODO 执行任务将recording记录通过websocket推送给当前用户
        pass

    def disconnect_push_recording(self):
        # TODO 中断将recording记录通过websocket推送给当前用户任务
        pass

    def push_message(self, request):
        user_id = self.request.user.id
        result_1 = websocket_push(
            1, message='content sent by api~'
        )
        os.system(f'python3 {BASE_DIR}/manage.py mitm &')
        return SuccessResponse(f"{result_1}")
