# -*- coding: utf-8 -*-

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django_restql.fields import DynamicSerializerMethodField
from rest_framework import serializers

from system.models import MessageCenter, Users, MessageCenterTargetUser
from utils.serializers import CustomModelSerializer

import logging


logger = logging.getLogger('django')


class MessageCenterSerializer(CustomModelSerializer):
    """
    消息中心-序列化器
    """
    role_info = DynamicSerializerMethodField()
    user_info = DynamicSerializerMethodField()
    dept_info = DynamicSerializerMethodField()
    is_read = serializers.BooleanField(read_only=True, source='target_user__is_read')

    def get_role_info(self, instance, parsed_query):
        roles = instance.target_role.all()
        # You can do what ever you want in here
        # `parsed_query` param is passed to BookSerializer to allow further querying
        from system.views.role import RoleSerializer
        serializer = RoleSerializer(
            roles,
            many=True,
            parsed_query=parsed_query
        )
        return serializer.data

    def get_user_info(self, instance, parsed_query):
        users = instance.target_user.all()
        # You can do what ever you want in here
        # `parsed_query` param is passed to BookSerializer to allow further querying
        from system.views.user import UserSerializer
        serializer = UserSerializer(
            users,
            many=True,
            parsed_query=parsed_query
        )
        return serializer.data

    def get_dept_info(self, instance, parsed_query):
        dept = instance.target_dept.all()
        # You can do what ever you want in here
        # `parsed_query` param is passed to BookSerializer to allow further querying
        from system.views.dept import DeptSerializer
        serializer = DeptSerializer(
            dept,
            many=True,
            parsed_query=parsed_query
        )
        return serializer.data

    class Meta:
        model = MessageCenter
        fields = "__all__"
        read_only_fields = ["id"]


class MessageCenterTargetUserSerializer(CustomModelSerializer):
    """
    目标用户序列化器-序列化器
    """

    class Meta:
        model = MessageCenterTargetUser
        fields = "__all__"
        read_only_fields = ["id"]


class MessageCenterTargetUserListSerializer(CustomModelSerializer):
    """
    目标用户序列化器-序列化器
    """
    is_read = serializers.SerializerMethodField()

    def get_is_read(self, instance):
        user_id = self.request.user.id
        message_center_id = instance.id
        queryset = MessageCenterTargetUser.objects.filter(message_center__id=message_center_id, users_id=user_id).first()
        if queryset:
            return queryset.is_read
        return False

    class Meta:
        model = MessageCenter
        fields = "__all__"
        read_only_fields = ["id"]


def websocket_push(user_id, message):
    """
    主动推送消息
    """
    username = "user_" + str(user_id)
    logger.info(f"code = 103, {message}")
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        username,
        {
            "type": "push.message",
            "json": message
        }
    )


class MessageCenterCreateSerializer(CustomModelSerializer):
    """
    消息中心-新增-序列化器
    """

    def save(self, **kwargs):
        data = super().save(**kwargs)
        initial_data = self.initial_data
        target_type = initial_data.get('target_type')
        # 在保存之前,根据目标类型,把目标用户查询出来并保存
        users = initial_data.get('target_user', [])
        if target_type in [1]:  # 按角色
            target_role = initial_data.get('target_role', [])
            users = Users.objects.filter(role__id__in=target_role).values_list('id', flat=True)
        if target_type in [2]:  # 按部门
            target_dept = initial_data.get('target_dept', [])
            users = Users.objects.filter(dept__id__in=target_dept).values_list('id', flat=True)
        if target_type in [3]:  # 系统通知
            users = Users.objects.values_list('id', flat=True)
        target_user_data = []
        for user in users:
            target_user_data.append({
                "message_center": data.id,
                "users": user
            })
        target_user_instance = MessageCenterTargetUserSerializer(
            data=target_user_data,
            many=True,
            request=self.request
        )
        target_user_instance.is_valid(raise_exception=True)
        target_user_instance.save()
        for user in users:
            unread_count = MessageCenterTargetUser.objects.filter(users__id=user, is_read=False).count()
            websocket_push(user, message={
                "sender": 'system',
                "contentType": 'SYSTEM',
                "content": '您有一条新消息~',
                "unread": unread_count
            }
                           )
        return data

    class Meta:
        model = MessageCenter
        fields = "__all__"
        read_only_fields = ["id"]
