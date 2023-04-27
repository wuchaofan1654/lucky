# # coding=utf-8
# """
# # Create by wuchaofan
# # At 2023/4/12
# # Current Dir custom/views
# """
# from custom.tasks import check_mitmproxy_status_task
#
# from system.utils.json_response import SuccessResponse
# from system.utils.viewset import CustomModelViewSet
# from system.views.message_center import websocket_push
#
#
# class MitmproxyViewSet(CustomModelViewSet):
#     def get(self, request):
#         user_id = self.request.user.id
#         result = check_mitmproxy_status_task()
#         try:
#             websocket_push(f"user_{user_id}", message={
#                 "sender": 'system',
#                 "contentType": 'TEXT',
#                 "content": f'{result}',
#             })
#         except Exception as err:
#             print(f"error: {err}")
#
#         return SuccessResponse(f"{result}")
#
