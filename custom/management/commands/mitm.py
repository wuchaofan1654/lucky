# -*- coding: utf-8 -*-
"""
Create by sandy at 14:25 23/12/2021
Description: ToDo
"""
import os
import time

from django.core.management import BaseCommand
import logging
from system.tasks import websocket_push

logger = logging.getLogger(__name__)
import django
django.setup()


class Command(BaseCommand):
    help = '开启mitmproxy拦截代理请求～'

    def handle(self, *args, **kwargs):
        for _ in range(1000):
            time.sleep(1)
            websocket_push.delay(1, message='command')

