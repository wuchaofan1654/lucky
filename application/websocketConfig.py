# -*- coding: utf-8 -*-
import logging
import urllib.parse

from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json

from channels.layers import get_channel_layer
from jwt import InvalidSignatureError
from rest_framework.request import Request

from application import settings
from system.models import Users
from system.serializers.message_center import MessageCenterTargetUserSerializer
from system.utils.serializers import CustomModelSerializer


send_dict = {}
logger = logging.getLogger('django')


# 发送消息结构体
def set_message(sender, msg_type, msg, unread=0):
    text = {
        'sender': sender,
        'contentType': msg_type,
        'content': msg,
        'unread': unread
    }
    return text


# 异步获取消息中心的目标用户
@database_sync_to_async
def _get_message_center_instance(message_id):
    from system.models import MessageCenter
    _MessageCenter = MessageCenter.objects.filter(id=message_id).values_list('target_user', flat=True)
    if _MessageCenter:
        return _MessageCenter
    else:
        return []


@database_sync_to_async
def _get_message_unread(user_id):
    """获取用户的未读消息数量"""
    from system.models import MessageCenterTargetUser
    count = MessageCenterTargetUser.objects.filter(users=user_id, is_read=False).count()
    return count or 0


def request_data(scope):
    query_string = scope.get('query_string', b'').decode('utf-8')
    qs = urllib.parse.parse_qs(query_string)
    return qs


class BasicWebSocket(AsyncJsonWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.service_uid = 0
        self.user_id = 0
        self.chat_group_name = 0

    async def connect(self):
        try:
            import jwt
            self.service_uid = self.scope["url_route"]["kwargs"]["service_uid"]
            decoded_result = jwt.decode(self.service_uid, settings.SECRET_KEY, algorithms=["HS256"])
            if decoded_result:
                self.user_id = decoded_result.get('user_id')
                self.chat_group_name = f"user_{self.user_id}"
                print(f"websocket连接成功：group_name={self.chat_group_name}")
                # 收到连接时候处理，
                await self.channel_layer.group_add(
                    self.chat_group_name,
                    self.channel_name
                )
                await self.accept()
                # 主动推送消息
                unread_count = await _get_message_unread(self.user_id)
                if unread_count == 0:
                    # 发送连接成功
                    await self.send_json(set_message('system', 'SYSTEM', '连接成功'))
                else:
                    await self.send_json(
                        set_message('system', 'SYSTEM', "请查看您的未读消息~",
                                    unread=unread_count))
        except InvalidSignatureError:
            await self.disconnect(None)

        except Exception as error:
            logger.exception(error)

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.chat_group_name, self.channel_name)
        logger.debug("连接关闭")
        try:
            await self.close(close_code)
        except Exception as e:
            logging.exception(e)
            pass


class MessageCenter(BasicWebSocket):
    """
    消息中心
    """
    async def receive(self, text_data=None, bytes_data=None):
        # 接受客户端的信息，你处理的函数
        text_data_json = json.loads(text_data)
        message_id = text_data_json.get('message_id', None)
        user_list = await _get_message_center_instance(message_id)
        for send_user in user_list:
            await self.channel_layer.group_send(
                "user_" + str(send_user),
                {'type': 'push.message', 'json': text_data_json}
            )

    async def push_message(self, event):
        """消息发送"""
        logger.info(f"开始执行 websocket push message: {event}")
        message = event
        logger.info(f"websocket pushed a message: {message}")
        await self.send(text_data=json.dumps(message))


class MessageCreateSerializer(CustomModelSerializer):
    """
    消息中心-新增-序列化器
    """

    class Meta:
        model = MessageCenter
        fields = "__all__"
        read_only_fields = ["id"]


def create_message_push(
        title: str,
        content: str,
        target_type: int = 0,
        target_user: list = list,
        target_dept=None,
        target_role=None,
        message=None,
        request=Request
):
    if message is None:
        message = {'contentType': 'INFO', 'content': '测试~'}
    if message is None:
        message = {"contentType": "INFO", "content": None}
    if target_role is None:
        target_role = []
    if target_dept is None:
        target_dept = []
    data = {
        "title": title,
        "content": content,
        "target_type": target_type,
        "target_user": target_user,
        "target_dept": target_dept,
        "target_role": target_role
    }
    message_center_instance = MessageCreateSerializer(data=data, request=request)
    message_center_instance.is_valid(raise_exception=True)
    message_center_instance.save()
    users = target_user or []
    if target_type in [1]:  # 按角色
        users = Users.objects.filter(role__id__in=target_role).values_list('id', flat=True)
    if target_type in [2]:  # 按部门
        users = Users.objects.filter(dept__id__in=target_dept).values_list('id', flat=True)
    if target_type in [3]:  # 系统通知
        users = Users.objects.values_list('id', flat=True)
    target_user_data = []
    for user in users:
        target_user_data.append({
            "message_center": message_center_instance.instance.id,
            "users": user
        })
    target_user_instance = MessageCenterTargetUserSerializer(data=target_user_data, many=True, request=request)
    target_user_instance.is_valid(raise_exception=True)
    target_user_instance.save()
    for user in users:
        username = "user_" + str(user)
        unread_count = async_to_sync(_get_message_unread)(user)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            username,
            {
                "type": "push.message",
                "json": {**message, 'unread': unread_count}
            }
        )
