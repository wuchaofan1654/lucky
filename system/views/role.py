# -*- coding: utf-8 -*-

"""
@author: lucky
@contact: QQ:382503189
@Created on: 2022/6/3 003 0:30
@Remark: 角色管理
"""
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from system.models import Role, Menu, Dept
from system.serializers import RoleSerializer, RoleCreateUpdateSerializer
from system.serializers.role import MenuPermissionSerializer
from system.utils.json_response import DetailResponse
from system.utils.viewset import CustomModelViewSet


class RoleViewSet(CustomModelViewSet):
    """
    角色管理接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    create_serializer_class = RoleCreateUpdateSerializer
    update_serializer_class = RoleCreateUpdateSerializer
    search_fields = ['name', 'key']

    @action(methods=['GET'], detail=False, permission_classes=[IsAuthenticated])
    def role_get_menu(self, request):
        """根据当前用户的角色返回角色拥有的菜单"""
        is_superuser = request.user.is_superuser
        is_admin = request.user.role.values_list('admin', flat=True)
        if is_superuser or True in is_admin:
            queryset = Menu.objects.filter(status=1).all()
        else:
            menu_id_list = request.user.role.values_list('menu', flat=True)
            queryset = Menu.objects.filter(id__in=menu_id_list)
        # queryset = self.filter_queryset(queryset)
        serializer = MenuPermissionSerializer(queryset, many=True, request=request)
        return DetailResponse(data=serializer.data)

    @action(methods=['GET'], detail=False, permission_classes=[IsAuthenticated])
    def data_scope(self, request):
        is_superuser = request.user.is_superuser
        role_queryset = Role.objects.filter(users__id=request.user.id).values_list('data_range', flat=True)
        if is_superuser:
            data = [
                {
                    "value": 0,
                    "label": '仅本人数据权限'
                },
                {
                    "value": 1,
                    "label": '本部门及以下数据权限'
                },
                {
                    "value": 2,
                    "label": '本部门数据权限'
                },
                {
                    "value": 3,
                    "label": '全部数据权限'
                },
                {
                    "value": 4,
                    "label": '自定义数据权限'
                }
            ]
        else:
            data = []
            data_range_list = list(set(role_queryset))
            for item in data_range_list:
                if item == 0:
                    data = [{
                        "value": 0,
                        "label": '仅本人数据权限'
                    }]
                elif item == 1:
                    data = [{
                        "value": 0,
                        "label": '仅本人数据权限'
                    }, {
                        "value": 1,
                        "label": '本部门及以下数据权限'
                    },
                        {
                            "value": 2,
                            "label": '本部门数据权限'
                        }]
                elif item == 2:
                    data = [{
                        "value": 0,
                        "label": '仅本人数据权限'
                    },
                        {
                            "value": 2,
                            "label": '本部门数据权限'
                        }]
                elif item == 3:
                    data = [{
                        "value": 0,
                        "label": '仅本人数据权限'
                    },
                        {
                            "value": 3,
                            "label": '全部数据权限'
                        }, ]
                elif item == 4:
                    data = [{
                        "value": 0,
                        "label": '仅本人数据权限'
                    },
                        {
                            "value": 4,
                            "label": '自定义数据权限'
                        }]
                else:
                    data = []
        return DetailResponse(data=data)

    @action(methods=['GET'], detail=False, permission_classes=[IsAuthenticated])
    def data_scope_dept(self, request):
        """根据当前角色获取部门信息"""
        is_superuser = request.user.is_superuser
        if is_superuser:
            queryset = Dept.objects.values('id', 'name', 'parent')
        else:
            dept_list = request.user.role.values_list('dept', flat=True)
            queryset = Dept.objects.filter(id__in=dept_list).values('id', 'name', 'parent')
        return DetailResponse(data=queryset)
