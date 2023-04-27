# -*- coding: utf-8 -*-

"""
@author: H0nGzA1
@contact: QQ:2505811377
@Remark: 部门管理
"""
from rest_framework import serializers

from system.models import Dept
from system.utils.serializers import CustomModelSerializer


class SimpleDeptSerializer(CustomModelSerializer):
    """
    部门-序列化器
    """
    class Meta:
        model = Dept
        fields = ('id', 'name')
        read_only_fields = ["id"]


class DeptSerializer(CustomModelSerializer):
    """
    部门-序列化器
    """
    parent_name = serializers.CharField(read_only=True, source='parent.name')
    status_label = serializers.SerializerMethodField()
    has_children = serializers.SerializerMethodField()
    has_child = serializers.SerializerMethodField()

    def get_has_child(self, instance):
        has_child = Dept.objects.filter(parent=instance.id)
        if has_child:
            return True
        return False

    def get_status_label(self, obj: Dept):
        if obj.status:
            return "启用"
        return "禁用"

    def get_has_children(self, obj: Dept):
        return Dept.objects.filter(parent_id=obj.id).count()

    class Meta:
        model = Dept
        fields = '__all__'
        read_only_fields = ["id"]


class DeptImportSerializer(CustomModelSerializer):
    """
    部门-导入-序列化器
    """

    class Meta:
        model = Dept
        fields = '__all__'
        read_only_fields = ["id"]


class DeptInitSerializer(CustomModelSerializer):
    """
    递归深度获取数信息(用于生成初始化json文件)
    """
    children = serializers.SerializerMethodField()

    def get_children(self, obj: Dept):
        data = []
        instance = Dept.objects.filter(parent_id=obj.id)
        if instance:
            serializer = DeptInitSerializer(instance=instance, many=True)
            data = serializer.data
        return data

    def save(self, **kwargs):
        instance = super().save(**kwargs)
        children = self.initial_data.get('children')
        if children:
            for menu_data in children:
                menu_data['parent'] = instance.id
                filter_data = {
                    "name": menu_data['name'],
                    "parent": menu_data['parent'],
                    "key": menu_data['key']
                }
                instance_obj = Dept.objects.filter(**filter_data).first()
                if instance_obj and not self.initial_data.get('reset'):
                    continue
                serializer = DeptInitSerializer(instance_obj, data=menu_data, request=self.request)
                serializer.is_valid(raise_exception=True)
                serializer.save()

        return instance

    class Meta:
        model = Dept
        fields = ['name', 'sort', 'owner', 'phone', 'email', 'status', 'parent', 'creator', 'dept_belong_id',
                  'children', 'key']
        extra_kwargs = {
            'creator': {'write_only': True},
            'dept_belong_id': {'write_only': True}
        }
        read_only_fields = ['id', 'children']


class DeptCreateUpdateSerializer(CustomModelSerializer):
    """
    部门管理 创建/更新时的列化器
    """

    def create(self, validated_data):
        value = validated_data.get('parent',None)
        if value is None:
            validated_data['parent'] = self.request.user.dept
        instance = super().create(validated_data)
        instance.dept_belong_id = instance.id
        instance.save()
        return instance

    class Meta:
        model = Dept
        fields = '__all__'
