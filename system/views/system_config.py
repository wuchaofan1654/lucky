# -*- coding: utf-8 -*-

"""
@author: lucky
@contact: QQ:382503189
@Created on: 2023/1/21 003 0:30
@Remark: 系统配置
"""
import django_filters
from django.db.models import Q
from django_filters.rest_framework import BooleanFilter
from rest_framework.views import APIView

from application import dispatch
from system.models import SystemConfig
from system.serializers import SystemConfigChildrenSerializer, SystemConfigCreateSerializer
from system.utils.json_response import DetailResponse, SuccessResponse, ErrorResponse
from system.utils.models import get_all_models_objects
from system.utils.viewset import CustomModelViewSet


class SystemConfigFilter(django_filters.rest_framework.FilterSet):
    """
    过滤器
    """
    parent__isnull = BooleanFilter(field_name='parent', lookup_expr="isnull")

    class Meta:
        model = SystemConfig
        fields = ['id', 'parent', 'status', 'parent__isnull']


class SystemConfigViewSet(CustomModelViewSet):
    """
    系统配置接口
    """
    queryset = SystemConfig.objects.order_by('sort', 'create_datetime')
    serializer_class = SystemConfigChildrenSerializer
    create_serializer_class = SystemConfigChildrenSerializer
    retrieve_serializer_class = SystemConfigChildrenSerializer
    # filter_fields = ['id','parent']
    filter_class = SystemConfigFilter

    def save_content(self, request):
        body = request.data
        data_mapping = {item['id']: item for item in body}
        for obj_id, data in data_mapping.items():
            instance_obj = SystemConfig.objects.filter(id=obj_id).first()
            if instance_obj is None:
                # return SystemConfig.objects.create(**data)
                serializer = SystemConfigCreateSerializer(data=data)
            else:
                serializer = SystemConfigCreateSerializer(instance_obj, data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
        return DetailResponse(msg="保存成功")

    def get_association_table(self, request):
        """
        获取所有的model及字段信息
        """
        res = [ele.get('table') for ele in get_all_models_objects().values()]
        return DetailResponse(msg="获取成功", data=res)

    def get_table_data(self, request, pk):
        """
        动态获取关联表的数据
        """
        instance = SystemConfig.objects.filter(id=pk).first()
        if instance is None:
            return ErrorResponse(msg="查询出错了~")
        setting = instance.setting
        if setting is None:
            return ErrorResponse(msg="查询出错了~")
        table = setting.get('table')  # 获取model名
        model = get_all_models_objects(table).get("object", {})
        # 自己判断一下不存在
        queryset = model.objects.values()
        body = request.query_params
        search_value = body.get('search', None)
        if search_value:
            search_fields = setting.get('searchField')
            filters = Q()
            filters.connector = 'OR'
            for item in search_fields:
                filed = '{0}__icontains'.format(item.get('field'))
                filters.children.append((filed, search_value))
            queryset = model.objects.filter(filters).values()
        page = self.paginate_queryset(queryset)
        if page is not None:
            return self.get_paginated_response(queryset)
        return SuccessResponse(msg="获取成功", data=queryset, total=len(queryset))

    def get_relation_info(self, request):
        """
        查询关联的模板信息
        """
        body = request.query_params
        var_name = body.get('varName', None)
        table = body.get('table', None)
        instance = SystemConfig.objects.filter(key=var_name, setting__table=table).first()
        if instance is None:
            return ErrorResponse(msg="未获取到关联信息")
        relation_id = body.get('relationIds', None)
        relation_ids = []
        if relation_id is None:
            return ErrorResponse(msg="未获取到关联信息")
        if instance.form_item_type in [13]:
            relation_ids = [relation_id]
        elif instance.form_item_type in [14]:
            relation_ids = relation_id.split(',')
        queryset = SystemConfig.objects.filter(value__in=relation_ids).first()
        if queryset is None:
            return ErrorResponse(msg="未获取到关联信息")
        serializer = SystemConfigChildrenSerializer(queryset.parent)
        return DetailResponse(msg="查询成功", data=serializer.data)


class InitSettingsViewSet(APIView):
    """
    获取初始化配置
    """
    authentication_classes = []
    permission_classes = []

    def filter_system_config_values(self, data: dict):
        """
        过滤系统初始化配置
        :param data:
        :return:
        """
        if not self.request.query_params.get('key', ''):
            return data
        new_data = {}
        for key in self.request.query_params.get('key', '').split('|'):
            if key:
                new_data.update(**dict(filter(lambda x: x[0].startswith(key), data.items())))
        return new_data

    def get(self, request):
        data = dispatch.get_system_config()
        if not data:
            dispatch.refresh_system_config()
            data = dispatch.get_system_config()
        # 不返回后端专用配置
        backend_config = [f"{ele.get('parent__key')}.{ele.get('key')}" for ele in
                          SystemConfig.objects.filter(status=False, parent_id__isnull=False).values('parent__key',
                                                                                                    'key')]
        data = dict(filter(lambda x: x[0] not in backend_config, data.items()))
        data = self.filter_system_config_values(data=data)
        return DetailResponse(data=data)
