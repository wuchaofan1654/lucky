# coding=utf-8
"""
# Create by wuchaofan 
# At 2023/4/20
# Current Dir custom/serializers
"""

from rest_framework import serializers

from system.serializers import SimpleUserSerializer
from system.utils.serializers import CustomModelSerializer
from custom.models import BugSet, Bug, BugRecord
from django_restql.fields import DynamicSerializerMethodField


class SimpleBugSetSerializer(CustomModelSerializer):
    """
    bug集合管理 简单序列化器
    """

    class Meta:
        model = BugSet
        fields = ('id', 'title', 'related_prd_id', 'create_datetime')


class SimpleBugSerializer(CustomModelSerializer):
    """
    bug管理 简单序列化器
    """

    class Meta:
        model = Bug
        fields = ('id', 'title', 'create_datetime')


class SimpleBugRecordSerializer(CustomModelSerializer):
    """
    bug流转明细管理 简单序列化器
    """

    class Meta:
        model = BugRecord
        fields = ('id', 'content', 'create_datetime')


# ================================================= #
# ************** bug管理 序列化器  ************** #
# ================================================= #
class BugSerializer(CustomModelSerializer):
    """
    bug管理 标准序列化器
    """
    follow_rd_info = DynamicSerializerMethodField()
    follow_qa_info = DynamicSerializerMethodField()

    belong_rd_name = serializers.CharField(
        source='belong_rd.name',
        read_only=True
    )
    belong_dept_name = serializers.CharField(
        source='belong_dept.name',
        read_only=True
    )
    bug_set_title = serializers.CharField(
        source='bug_set.title',
        read_only=True
    )
    close_qa_name = serializers.CharField(
        source='close_qa.name',
        read_only=True
    )

    def get_follow_qa_info(self, instance, parsed_query):
        queryset = instance.follow_qa.all()
        serializer = SimpleUserSerializer(
            queryset,
            many=True,
            parsed_query=parsed_query
        )
        return serializer.data

    def get_follow_rd_info(self, instance, parsed_query):
        queryset = instance.follow_rd.all()
        serializer = SimpleUserSerializer(
            queryset,
            many=True,
            parsed_query=parsed_query
        )
        return serializer.data

    def save(self, **kwargs):
        instance = super().save(**kwargs)
        return instance

    class Meta:
        model = Bug
        exclude = ('description', 'creator', 'modifier')


class BugCreateUpdateSerializer(CustomModelSerializer):
    """
    bug管理 创建/更新时的列化器
    """

    def validate(self, attrs: dict):
        return super().validate(attrs)

    class Meta:
        model = Bug
        fields = '__all__'


class ExportBugProfileSerializer(CustomModelSerializer):
    """
    录制记录导出 序列化器
    """

    class Meta:
        model = Bug
        fields = '__all__'


class BugImportSerializer(CustomModelSerializer):
    def save(self, **kwargs):
        data = super().save(**kwargs)
        data.save()
        return data

    class Meta:
        model = Bug
        exclude = (
            "bug_set",
            "title",
            "desc",
            "cause_reason",
            "level"
        )


# ================================================= #
# ************** bug集合管理 序列化器  ************** #
# ================================================= #
class BugSetSerializer(CustomModelSerializer):
    """
    bug集合管理 标准序列化器
    """

    related_bug_list = serializers.SerializerMethodField(read_only=True)
    related_bug_cnt = serializers.SerializerMethodField(read_only=True)

    def get_related_bug_list(self, instance):
        queryset = Bug.objects.filter(bug_set=instance).values('id', 'title')
        return SimpleBugSerializer(queryset, many=True).data

    def get_related_bug_cnt(self, instance):
        return len(Bug.objects.filter(bug_set=instance).values('id'))

    class Meta:
        model = BugSet
        exclude = ('description', 'creator', 'modifier')


class BugSetCreateUpdateSerializer(CustomModelSerializer):
    """
    bug集合管理 创建/更新时的列化器
    """

    def validate(self, attrs: dict):
        return super().validate(attrs)

    class Meta:
        model = BugSet
        fields = '__all__'


# ================================================= #
# ************** bug流转明细管理 序列化器  ************** #
# ================================================= #

class BugRecordSerializer(CustomModelSerializer):
    """
    bug流转明细管理 简单序列化器
    """
    class Meta:
        model = BugRecord
        exclude = ('description', 'modifier')


class BugRecordCreateUpdateSerializer(CustomModelSerializer):
    """
    bug流转明细管理 创建/更新时的列化器
    """
    def validate(self, attrs: dict):
        return super().validate(attrs)

    class Meta:
        model = BugRecord
        fields = '__all__'
