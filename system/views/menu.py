# -*- coding: utf-8 -*-

"""
@author: lucky
@contact: QQ:382503189
@Created on: 2022/6/1 001 22:38
@Remark: 菜单模块
"""
from rest_framework.decorators import action

from system.models import Menu, MenuButton
from system.serializers import MenuSerializer
from system.serializers.menu import WebRouterSerializer, MenuCreateSerializer
from system.serializers import MenuButtonSerializer, MenuButtonCreateUpdateSerializer
from system.utils.json_response import SuccessResponse
from system.utils.viewset import CustomModelViewSet


class MenuViewSet(CustomModelViewSet):
    """
    菜单管理接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    create_serializer_class = MenuCreateSerializer
    update_serializer_class = MenuCreateSerializer
    search_fields = ['name', 'status']
    filter_fields = ['parent', 'name', 'status', 'is_link', 'visible', 'cache', 'is_catalog']
    # extra_filter_backends = []

    @action(methods=['GET'], detail=False, permission_classes=[])
    def web_router(self, request):
        """用于前端获取当前角色的路由"""
        user = request.user
        queryset = self.queryset.filter(status=1)
        if not user.is_superuser:
            menu_ids = user.role.values_list('menu__id', flat=True)
            queryset = Menu.objects.filter(id__in=menu_ids, status=1)
        serializer = WebRouterSerializer(queryset, many=True, request=request)
        data = serializer.data
        return SuccessResponse(data=data, total=len(data), msg="获取成功")

    def list(self, request):
        """懒加载"""
        params = request.query_params
        parent = params.get('parent', None)
        if params:
            if parent:
                queryset = self.queryset.filter(parent=parent)
            else:
                queryset = self.queryset
        else:
            queryset = self.queryset.filter(parent__isnull=True)
        queryset = self.filter_queryset(queryset)
        serializer = MenuSerializer(queryset, many=True, request=request)
        data = serializer.data
        return SuccessResponse(data=data)


class MenuButtonViewSet(CustomModelViewSet):
    """
    菜单按钮接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = MenuButton.objects.all()
    serializer_class = MenuButtonSerializer
    create_serializer_class = MenuButtonCreateUpdateSerializer
    update_serializer_class = MenuButtonCreateUpdateSerializer
    extra_filter_backends = []
