
# -*- coding: utf-8 -*-
from rest_framework import serializers

from system.models import Area
from utils.serializers import CustomModelSerializer


class AreaSerializer(CustomModelSerializer):
    """
    地区-序列化器
    """
    f_code_count = serializers.SerializerMethodField(read_only=True)

    def get_f_code_count(self, instance: Area):
        return Area.objects.filter(f_code=instance).count()

    class Meta:
        model = Area
        fields = "__all__"
        read_only_fields = ["id"]


class AreaCreateUpdateSerializer(CustomModelSerializer):
    """
    地区管理 创建/更新时的列化器
    """

    class Meta:
        model = Area
        fields = '__all__'
