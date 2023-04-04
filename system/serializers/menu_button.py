# -*- coding: utf-8 -*-

"""
@author: 猿小天
@contact: QQ:1638245306
@Created on: 2021/6/1 001 22:38
@Remark: 菜单模块
"""

from system.models import MenuButton
from utils.serializers import CustomModelSerializer


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
