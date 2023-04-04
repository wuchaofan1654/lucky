from django.urls import path
from rest_framework import routers

from system.views.api_white_list import ApiWhiteListViewSet
from system.views.area import AreaViewSet
from system.views.dept import DeptViewSet
from system.views.dictionary import DictionaryViewSet
from system.views.file_list import FileViewSet
from system.views.login_log import LoginLogViewSet
from system.views.menu import MenuViewSet
from system.views.menu import MenuButtonViewSet
from system.views.message_center import MessageCenterViewSet
from system.views.operation_log import OperationLogViewSet
from system.views.role import RoleViewSet
from system.views.system_config import SystemConfigViewSet
from system.views.user import UserViewSet

system_url = routers.SimpleRouter()
system_url.register(r'menu', MenuViewSet)
system_url.register(r'menu_button', MenuButtonViewSet)
system_url.register(r'role', RoleViewSet)
system_url.register(r'dept', DeptViewSet)
system_url.register(r'user', UserViewSet)
system_url.register(r'operation_log', OperationLogViewSet)
system_url.register(r'dictionary', DictionaryViewSet)
system_url.register(r'area', AreaViewSet)
system_url.register(r'file', FileViewSet)
system_url.register(r'api_white_list', ApiWhiteListViewSet)
system_url.register(r'system_config', SystemConfigViewSet)
system_url.register(r'message_center', MessageCenterViewSet)

urlpatterns = [
    path('system_config/save_content/', SystemConfigViewSet.as_view({'put': 'save_content'})),
    path('system_config/get_association_table/', SystemConfigViewSet.as_view({'get': 'get_association_table'})),
    path('system_config/get_table_data/<int:pk>/', SystemConfigViewSet.as_view({'get': 'get_table_data'})),
    path('system_config/get_relation_info/', SystemConfigViewSet.as_view({'get': 'get_relation_info'})),
    path('login_log/', LoginLogViewSet.as_view({'get': 'list'})),
    path('login_log/<int:pk>/', LoginLogViewSet.as_view({'get': 'retrieve'})),
    path('dept_lazy_tree/', DeptViewSet.as_view({'get': 'dept_lazy_tree'})),
]
urlpatterns += system_url.urls
