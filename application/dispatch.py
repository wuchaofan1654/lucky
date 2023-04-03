#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf import settings
from django.db import connection
import logging


logger = logging.getLogger('django')


# ================================================= #
# ******************** 初始化 ******************** #
# ================================================= #
def _get_all_dictionary():
    from system.models import Dictionary

    queryset = Dictionary.objects.filter(status=True, is_value=False)
    data = []
    for instance in queryset:
        data.append(
            {
                "id": instance.id,
                "value": instance.value,
                "children": list(
                    Dictionary.objects.filter(parent=instance.id)
                    .filter(status=1)
                    .values("label", "value", "type", "color")
                ),
            }
        )
    return {ele.get("value"): ele for ele in data}


def _get_all_system_config():
    data = {}
    from system.models import SystemConfig

    system_config_obj = (
        SystemConfig.objects.filter(parent_id__isnull=False)
        .values("parent__key", "key", "value", "form_item_type")
        .order_by("sort")
    )
    for system_config in system_config_obj:
        value = system_config.get("value", "")
        if value and system_config.get("form_item_type") == 7:
            value = value[0].get("url")
        if value and system_config.get("form_item_type") == 11:
            new_value = []
            for ele in value:
                new_value.append({
                    "key": ele.get('key'),
                    "title": ele.get('title'),
                    "value": ele.get('value'),
                })
            new_value.sort(key=lambda s: s["key"])
            value = new_value
        data[f"{system_config.get('parent__key')}.{system_config.get('key')}"] = value
    return data


def init_dictionary():
    """
    初始化字典配置
    :return:
    """
    try:
        settings.DICTIONARY_CONFIG = _get_all_dictionary()
    except Exception as e:
        logger.exception(e)
        print("请先进行数据库迁移!")
    return


def init_system_config():
    """
    初始化系统配置
    :param name:
    :return:
    """
    try:
        settings.SYSTEM_CONFIG = _get_all_system_config()
    except Exception as e:
        logger.exception(e)
        print("请先进行数据库迁移!")
    return


def refresh_dictionary():
    """
    刷新字典配置
    :return:
    """
    settings.DICTIONARY_CONFIG = _get_all_dictionary()


def refresh_system_config():
    """
    刷新系统配置
    :return:
    """
    settings.SYSTEM_CONFIG = _get_all_system_config()


# ================================================= #
# ******************** 字典管理 ******************** #
# ================================================= #
def get_dictionary_config(schema_name=None):
    """
    获取字典所有配置
    :param schema_name: 对应字典配置的租户schema_name值
    :return:
    """
    if not settings.DICTIONARY_CONFIG:
        refresh_dictionary()

    dictionary_config = settings.DICTIONARY_CONFIG

    return dictionary_config or {}


def get_dictionary_values(key, schema_name=None):
    """
    获取字典数据数组
    :param key: 对应字典配置的key值(字典编号)
    :param schema_name: 对应字典配置的租户schema_name值
    :return:
    """
    dictionary_config = get_dictionary_config(schema_name)
    return dictionary_config.get(key)


def get_dictionary_label(key, name, schema_name=None):
    """
    获取获取字典label值
    :param key: 字典管理中的key值(字典编号)
    :param name: 对应字典配置的value值
    :param schema_name: 对应字典配置的租户schema_name值
    :return:
    """
    children = get_dictionary_values(key, schema_name) or []
    for ele in children:
        if ele.get("value") == str(name):
            return ele.get("label")
    return ""


# ================================================= #
# ******************** 系统配置 ******************** #
# ================================================= #
def get_system_config(schema_name=None):
    """
    获取系统配置中所有配置
    1.只传父级的key，返回全部子级，{ "父级key.子级key" : "值" }
    2."父级key.子级key"，返回子级值
    :param schema_name: 对应字典配置的租户schema_name值
    :return:
    """
    if not settings.SYSTEM_CONFIG:
        refresh_system_config()

    dictionary_config = settings.SYSTEM_CONFIG

    return dictionary_config or {}


def get_system_config_values(key, schema_name=None):
    """
    获取系统配置数据数组
    :param key: 对应系统配置的key值(字典编号)
    :param schema_name: 对应系统配置的租户schema_name值
    :return:
    """
    system_config = get_system_config(schema_name)
    return system_config.get(key)


def get_system_config_label(key, name, schema_name=None):
    """
    获取获取系统配置label值
    :param key: 系统配置中的key值(字典编号)
    :param name: 对应系统配置的value值
    :param schema_name: 对应系统配置的租户schema_name值
    :return:
    """
    children = get_system_config_values(key, schema_name) or []
    for ele in children:
        if ele.get("value") == str(name):
            return ele.get("label")
    return ""
