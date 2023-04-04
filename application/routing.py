# -*- coding: utf-8 -*-
from django.urls import path
from application.websocketConfig import MessageCenter

websocket_urlpatterns = [
    # consumers.BasicWebSocket 是该路由的消费者
    path('ws/<str:service_uid>/', MessageCenter.as_asgi()),
]

