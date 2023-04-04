# -*- coding: utf-8 -*-

"""
@author: H0nGzA1
@contact: QQ:2505811377
@Remark: 部门管理
"""
from rest_framework.decorators import action

from system.models import Dept
from system.serializers import DeptSerializer, DeptCreateUpdateSerializer, DeptImportSerializer
from utils.json_response import DetailResponse, SuccessResponse
from utils.permission import AnonymousUserPermission
from utils.viewset import CustomModelViewSet


class DeptViewSet(CustomModelViewSet):
    """
    部门管理接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = Dept.objects.all()
    serializer_class = DeptSerializer
    create_serializer_class = DeptCreateUpdateSerializer
    update_serializer_class = DeptCreateUpdateSerializer
    filter_fields = ['name', 'id', 'parent']
    search_fields = []
    # extra_filter_backends = []
    import_serializer_class = DeptImportSerializer
    import_field_dict = {
        "name": "部门名称",
        "key": "部门标识",
    }

    def list(self, request, *args, **kwargs):
        # 如果懒加载，则只返回父级
        params = request.query_params
        parent = params.get('parent', None)
        if params:
            if parent:
                queryset = self.queryset.filter(status=True, parent=parent)
            else:
                queryset = self.queryset.filter(status=True)
        else:
            queryset = self.queryset.filter(status=True, parent__isnull=True)
        queryset = self.filter_queryset(queryset)
        serializer = DeptSerializer(queryset, many=True, request=request)
        data = serializer.data
        return SuccessResponse(data=data)

    def dept_lazy_tree(self, request, *args, **kwargs):
        parent = self.request.query_params.get('parent')
        is_superuser = request.user.is_superuser
        if is_superuser:
            queryset = Dept.objects.values('id', 'name', 'parent')
        else:
            data_range = request.user.role.values_list('data_range', flat=True)
            user_dept_id = request.user.dept.id
            dept_list = [user_dept_id]
            data_range_list = list(set(data_range))
            for item in data_range_list:
                if item in [0,2]:
                    dept_list = [user_dept_id]
                elif item == 1:
                    dept_list = Dept.recursion_dept_info(dept_id=user_dept_id)
                elif item == 3:
                    dept_list = Dept.objects.values_list('id',flat=True)
                elif item == 4:
                    dept_list = request.user.role.values_list('dept',flat=True)
                else:
                    dept_list = []
            queryset = Dept.objects.filter(id__in=dept_list).values('id', 'name', 'parent')
        return DetailResponse(data=queryset, msg="获取成功")

    @action(methods=["GET"], detail=False, permission_classes=[AnonymousUserPermission])
    def all_dept(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        data = queryset.filter(status=True).order_by('sort').values('name', 'id', 'parent')
        return DetailResponse(data=data, msg="获取成功")
