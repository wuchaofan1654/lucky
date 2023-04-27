import datetime
import random

from system.models import Users, Dept
from system.utils.json_response import DetailResponse
from system.utils.viewset import CustomModelViewSet
from custom.models import BugSet, Bug, BugRecord
from custom.serializers import BugSetSerializer, BugSetCreateUpdateSerializer
from custom.serializers import BugSerializer, BugCreateUpdateSerializer, ExportBugProfileSerializer, BugImportSerializer
from custom.serializers import BugRecordSerializer, BugRecordCreateUpdateSerializer
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated


class BugSetModelViewSet(CustomModelViewSet):
    """
    bug集合模型 的CRUD视图
    """
    queryset = BugSet.objects.all()
    serializer_class = BugSetSerializer
    create_serializer_class = BugSetCreateUpdateSerializer
    update_serializer_class = BugSetCreateUpdateSerializer

    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated])
    def batch_create_bug_set(self, request):
        """批量创建bug_set"""
        for _ in range(10):
            BugSet.objects.create(
                title=f'bug合集标题-{_}',
                desc=f'bug合集描述-{_}',
                related_prd_id='SY-P-20233201'
            ).save()
        return DetailResponse(data=None, msg="批量创建bug_set成功")


class BugModelViewSet(CustomModelViewSet):
    """
    bug模型 的CRUD视图
    """
    queryset = Bug.objects.all()
    serializer_class = BugSerializer
    create_serializer_class = BugCreateUpdateSerializer
    update_serializer_class = BugCreateUpdateSerializer

    # 导出
    export_field_label = fields = {
        "title": "标题",
        "desc": "描述",
        "level": "等级",
        "status": "状态",
        'cause_reason': "问题原因",
        'create_datetime': "创建时间",
        'solve_datetime': "解决时间",
        'close_datetime': "关闭时间"
    }
    export_serializer_class = ExportBugProfileSerializer
    import_serializer_class = BugImportSerializer

    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated])
    def batch_create_bug(self, request):
        """批量创建bug"""
        for _ in range(10000):
            bug = Bug.objects.create(
                title=f'bug标题-{datetime.datetime.now()}',
                desc=f'bug描述-{datetime.datetime.now()}',
                solve_status=random.randint(1, 4),
                cause_reason=random.randint(1, 8),
                resource='',
                level=random.randint(1, 4)
            )
            bug_set_id = random.randint(1, 10000)
            bug.bug_set = BugSet.objects.filter(id=bug_set_id).first()

            bug.belong_dept = Dept.objects.filter(id=1).first()
            bug.belong_rd = Users.objects.filter(id=random.randint(6, 8)).first()
            bug.close_qa = Users.objects.filter(id=5).first()

            bug.follow_qa.add(5)
            bug.follow_rd.add(random.randint(6, 8))
            bug.save()

        return DetailResponse(data=None, msg="批量创建bug成功")


class BugRecordModelViewSet(CustomModelViewSet):
    """
    bug流程明细模型 的CRUD视图
    """
    queryset = BugRecord.objects.all()
    serializer_class = BugRecordSerializer
    create_serializer_class = BugRecordCreateUpdateSerializer
    update_serializer_class = BugRecordCreateUpdateSerializer

    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated])
    def batch_create_bug_record(self, request):
        """批量创建bug"""
        for _ in range(10000):
            queryset = Bug.objects.filter(id__gt=1)
            for query in queryset:
                for _ in range(random.randint(1, 100)):
                    BugRecord.objects.create(
                        bug=query,
                        operator=Users.objects.get(id=5),
                        content=f'<p>操作明细{datetime.datetime.today()}</p>'
                    ).save()

        return DetailResponse(data=None, msg="批量创建bugRecord成功")
