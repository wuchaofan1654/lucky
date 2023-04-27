# -*- coding: utf-8 -*-

"""
@author: lucky
@contact: QQ:382503189
@Created on: 2022/6/1 001 22:38
@Remark: 菜单模块
"""
from rest_framework import serializers

from system.models import Menu, MenuButton
from system.utils.serializers import CustomModelSerializer


class MenuSerializer(CustomModelSerializer):
    """
    菜单表的简单序列化器
    """
    menu_permission = serializers.SerializerMethodField(read_only=True)
    has_child = serializers.SerializerMethodField()

    def get_menu_permission(self, instance):
        queryset = instance.menu_permission.order_by('-name').values_list('name', flat=True)
        if queryset:
            return queryset
        else:
            return None

    def get_has_child(self, instance):
        has_child = Menu.objects.filter(parent=instance.id)
        if has_child:
            return True

        return False

    class Meta:
        model = Menu
        fields = "__all__"
        read_only_fields = ["id"]


class MenuCreateSerializer(CustomModelSerializer):
    """
    菜单表的创建序列化器
    """
    name = serializers.CharField(required=False)

    class Meta:
        model = Menu
        fields = "__all__"
        read_only_fields = ["id"]


class MenuInitSerializer(CustomModelSerializer):
    """
    递归深度获取数信息(用于生成初始化json文件)
    """
    name = serializers.CharField(required=False)
    children = serializers.SerializerMethodField()
    menu_button = serializers.SerializerMethodField()

    def get_children(self, obj: Menu):
        data = []
        instance = Menu.objects.filter(parent_id=obj.id)
        if instance:
            serializer = MenuInitSerializer(instance=instance, many=True)
            data = serializer.data
        return data

    def get_menu_button(self, obj: Menu):
        data = []
        print(obj)
        instance = obj.menu_permission.order_by('method')
        if instance:
            data = list(instance.values('name', 'value', 'api', 'method'))
        return data

    def save(self, **kwargs):
        instance = super().save(**kwargs)
        children = self.initial_data.get('children')
        menu_button = self.initial_data.get('menu_button')
        # 菜单表
        if children:
            for menu_data in children:
                menu_data['parent'] = instance.id
                filter_data = {
                    "name": menu_data['name'],
                    "web_path": menu_data['web_path'],
                    "component": menu_data['component'],
                    "component_name": menu_data['component_name'],
                }
                instance_obj = Menu.objects.filter(**filter_data).first()
                if instance_obj and not self.initial_data.get('reset'):
                    continue
                serializer = MenuInitSerializer(instance_obj, data=menu_data, request=self.request)
                serializer.is_valid(raise_exception=True)
                serializer.save()
        # 菜单按钮
        if menu_button:
            for menu_button_data in menu_button:
                menu_button_data['menu'] = instance.id
                filter_data = {
                    "menu": menu_button_data['menu'],
                    "value": menu_button_data['value']
                }
                instance_obj = MenuButton.objects.filter(**filter_data).first()
                serializer = MenuButtonInitSerializer(instance_obj, data=menu_button_data, request=self.request)
                serializer.is_valid(raise_exception=True)
                serializer.save()
        return instance

    class Meta:
        model = Menu
        fields = ['name', 'icon', 'sort', 'is_link', 'is_catalog', 'web_path', 'component', 'component_name', 'status',
                  'cache', 'visible', 'parent', 'children', 'menu_button', 'creator', 'dept_belong_id']
        extra_kwargs = {
            'creator': {'write_only': True},
            'dept_belong_id': {'write_only': True}
        }
        read_only_fields = ['id', 'children']


class WebRouterSerializer(CustomModelSerializer):
    """
    前端菜单路由的简单序列化器
    """
    path = serializers.CharField(source="web_path")
    title = serializers.CharField(source="name")
    menu_permission = serializers.SerializerMethodField(read_only=True)

    def get_menu_permission(self, instance):
        # 判断是否是超级管理员
        if self.request.user.is_superuser:
            return instance.menu_permission.values_list('value', flat=True)
        else:
            # 根据当前角色获取权限按钮id集合
            permission_ids = self.request.user.role.values_list('permission', flat=True)
            queryset = instance.menu_permission.filter(
                id__in=permission_ids, menu=instance.id).values_list('value', flat=True)
            if queryset:
                return queryset
            else:
                return None

    class Meta:
        model = Menu
        fields = ('id', 'parent', 'icon', 'sort', 'path', 'name', 'title', 'is_link', 'is_catalog', 'web_path',
                  'component', 'component_name', 'cache', 'visible', 'menu_permission')
        read_only_fields = ["id"]


class MenuButtonSerializer(CustomModelSerializer):
    """
    菜单按钮-序列化器
    """

    class Meta:
        model = MenuButton
        fields = ['id', 'name', 'value', 'api', 'method']
        read_only_fields = ["id"]


class MenuButtonInitSerializer(CustomModelSerializer):
    """
    初始化菜单按钮-序列化器
    """

    class Meta:
        model = MenuButton
        fields = ['id', 'name', 'value', 'api', 'method', 'menu']
        read_only_fields = ["id"]


class MenuButtonCreateUpdateSerializer(CustomModelSerializer):
    """
    初始化菜单按钮-序列化器
    """

    class Meta:
        model = MenuButton
        fields = "__all__"
        read_only_fields = ["id"]

