# -*- coding: utf-8 -*-
"""
Create by sandy at 19:54 14/03/2022
Description: ToDo
"""
from django.urls import path

from custom.consumers import WebsocketConsumer

websocket_urlpatterns = [
    path('ws/<str:topic>/<int:service_uid>/', WebsocketConsumer.as_asgi()),
]
