# -*- coding: utf-8 -*-

from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from system.models import MessageCenter, MessageCenterTargetUser
from system.serializers import MessageCenterSerializer, MessageCenterCreateSerializer, \
    MessageCenterTargetUserListSerializer
from custom.tasks import websocket_push
from system.utils.json_response import SuccessResponse, DetailResponse
from system.utils.viewset import CustomModelViewSet


class MessageCenterViewSet(CustomModelViewSet):
    """
    消息中心接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """
    queryset = MessageCenter.objects.order_by('create_datetime')
    serializer_class = MessageCenterSerializer
    create_serializer_class = MessageCenterCreateSerializer
    extra_filter_backends = []

    def get_queryset(self):
        if self.action == 'list':
            return MessageCenter.objects.filter(creator=self.request.user.id).all()
        return MessageCenter.objects.all()

    def retrieve(self, request, *args, **kwargs):
        """
        重写查看
        """
        pk = kwargs.get('pk')
        user_id = self.request.user.id
        print(f"1==========={self.request.user}, {user_id}")
        queryset = MessageCenterTargetUser.objects.filter(users__id=user_id, message_center__id=pk).first()
        if queryset:
            queryset.is_read = True
            queryset.save()
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        # 主动推送消息
        unread_count = MessageCenterTargetUser.objects.filter(users__id=user_id, is_read=False).count()
        websocket_push(user_id, message={
            "sender": 'system',
            "contentType": 'TEXT',
            "content": '您查看了一条消息~',
            "unread": unread_count
        })
        return DetailResponse(data=serializer.data, msg="获取成功")

    @action(methods=['GET'], detail=False, permission_classes=[IsAuthenticated])
    def get_self_receive(self, request):
        """
        获取接收到的消息
        """
        self_user_id = self.request.user.id
        # queryset = MessageCenterTargetUser.objects.filter(users__id=self_user_id).order_by('-create_datetime')
        queryset = MessageCenter.objects.filter(target_user__id=self_user_id)
        # queryset = self.filter_queryset(queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = MessageCenterTargetUserListSerializer(page, many=True, request=request)
            return self.get_paginated_response(serializer.data)
        serializer = MessageCenterTargetUserListSerializer(queryset, many=True, request=request)
        return SuccessResponse(data=serializer.data, msg="获取成功")

    @action(methods=['GET'], detail=False, permission_classes=[IsAuthenticated])
    def get_newest_msg(self, request):
        """
        获取最新的一条消息
        """
        self_user_id = self.request.user.id
        queryset = MessageCenterTargetUser.objects.filter(users__id=self_user_id).order_by('create_datetime').last()
        data = None
        if queryset:
            serializer = MessageCenterTargetUserListSerializer(queryset.message_center, many=False, request=request)
            data = serializer.data
        return DetailResponse(data=data, msg="获取成功")
