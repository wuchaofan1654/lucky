# -*- coding: utf-8 -*-
"""
Create by sandy at 11:25 25/03/2022
Description: ToDo
"""

from channels.generic.websocket import AsyncWebsocketConsumer
import json
from application import settings
import logging


logger = logging.getLogger('django')


class BasicConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # 统一的group_name生成方式：device_id_topic_name
        import jwt
        self.service_uid = self.scope["url_route"]["kwargs"]["service_uid"]
        decoded_result = jwt.decode(self.service_uid, settings.SECRET_KEY, algorithms=["HS256"])
        if decoded_result:
            self.user_id = decoded_result.get('user_id')
            self.group_name = f"user_{self.user_id}"
            await self.channel_layer.group_add(
                self.group_name,
                self.channel_name
            )
            await self.accept()
            logger.info(f"ws[{self.group_name}]连接成功：～")

    async def disconnect(self, close_code):
        # 关闭前执行操作
        await self.channel_layer.group_discard(
            self.scope['group_name'],
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(
            self.scope['group_name'],
            {
                'type': 'push.message',
                'message': message
            }
        )

    async def push_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message']
        }))
