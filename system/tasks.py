# coding=utf-8
"""
# Create by wuchaofan 
# At 2023/4/13
# Current Dir system
"""

import logging
from application.celery import app
from asgiref.sync import async_to_sync, sync_to_async
from channels.layers import get_channel_layer


logger = logging.getLogger('django')


@app.task()
def websocket_push(user_id, message):
    """TODO 异步执行不生效"""
    username = f"user_{user_id}"
    channel_layer = get_channel_layer()
    logger.info(f"{channel_layer}开始给username = {username} 发送消息: {message}～")
    try:
        async_to_sync(channel_layer.group_send)(
            username, {
                "type": "push.message",
                "message": message
            }
        )
    except Exception as err:
        logger.error(err)
    logger.info(f"发送消息完成～")

