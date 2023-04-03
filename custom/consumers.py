# -*- coding: utf-8 -*-
"""
Create by sandy at 11:25 25/03/2022
Description: ToDo
"""

from channels.generic.websocket import AsyncWebsocketConsumer

import json

from utils.encrypt_util import encrypt


class WebsocketConsumer(AsyncWebsocketConsumer):
    def _topic_name(self):
        pass

    def gen_group_name(self):
        device_id = self.scope['url_route']['kwargs'].get('device_id', 0)
        return encrypt(f'{device_id}_{self._topic_name()}')

    async def connect(self):
        # 统一的group_name生成方式：device_id_topic_name
        self.scope['group_name'] = self.gen_group_name()
        await self.channel_layer.group_add(
            self.scope['group_name'],
            self.channel_name
        )
        await self.accept()

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
                'type': 'send.message',
                'message': message
            }
        )

    async def send_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message']
        }))
