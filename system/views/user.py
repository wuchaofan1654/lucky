import hashlib

from django.contrib.auth.hashers import make_password
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.db import connection
from application import dispatch
from system.models import Users, Role, Dept
from system.serializers import UserSerializer, UserCreateSerializer, UserUpdateSerializer, ExportUserProfileSerializer, \
    UserProfileImportSerializer, UserInfoUpdateSerializer
from system.utils.json_response import ErrorResponse, DetailResponse
from system.utils.viewset import CustomModelViewSet


def recursion(instance, parent, result):
    new_instance = getattr(instance, parent, None)
    res = []
    data = getattr(instance, result, None)
    if data:
        res.append(data)
    if new_instance:
        array = recursion(new_instance, parent, result)
        res += (array)
    return res


class UserViewSet(CustomModelViewSet):
    """
    用户接口
    list:查询
    create:新增
    update:修改
    retrieve:单例
    destroy:删除
    """

    queryset = Users.objects.exclude(is_superuser=1).all()
    serializer_class = UserSerializer
    create_serializer_class = UserCreateSerializer
    update_serializer_class = UserUpdateSerializer
    # filter_fields = ["name", "username", "gender", "is_active", "dept", "user_type"]
    filter_fields = {
        "name": ["exact"],
        "mobile": ["exact"],
        "username": ["exact"],
        "gender": ["icontains"],
        "is_active": ["icontains"],
        "dept": ["exact"],
        "user_type": ["exact"],
    }
    search_fields = ["username", "name", "gender", "dept__name", "role__name"]
    # 导出
    export_field_label = {
        "username": "用户账号",
        "name": "用户名称",
        "email": "用户邮箱",
        "mobile": "手机号码",
        "gender": "用户性别",
        "is_active": "帐号状态",
        "last_login": "最后登录时间",
        "dept_name": "部门名称",
        "dept_owner": "部门负责人",
    }
    export_serializer_class = ExportUserProfileSerializer
    # 导入
    import_serializer_class = UserProfileImportSerializer
    import_field_dict = {
        "username": "登录账号",
        "name": "用户名称",
        "email": "用户邮箱",
        "mobile": "手机号码",
        "gender": {
            "title": "用户性别",
            "choices": {
                "data": {"未知": 2, "男": 1, "女": 0},
            }
        },
        "is_active": {
            "title": "帐号状态",
            "choices": {
                "data": {"启用": True, "禁用": False},
            }
        },
        "password": "登录密码",
        "dept": {"title": "部门", "choices": {"queryset": Dept.objects.filter(status=True), "values_name": "name"}},
        "role": {"title": "角色", "choices": {"queryset": Role.objects.filter(status=True), "values_name": "name"}},
    }

    @action(methods=["GET"], detail=False, permission_classes=[IsAuthenticated])
    def user_info(self, request):
        """获取当前用户信息"""
        user = request.user
        result = {
            "id": user.id,
            "username": user.username,
            "name": user.name,
            "mobile": user.mobile,
            "user_type": user.user_type,
            "gender": user.gender,
            "email": user.email,
            "avatar": user.avatar,
            "dept": user.dept_id,
            "is_superuser": user.is_superuser,
            "role": user.role.values_list('id', flat=True),
        }
        if hasattr(connection, 'tenant'):
            result['tenant_id'] = connection.tenant and connection.tenant.id
            result['tenant_name'] = connection.tenant and connection.tenant.name
        dept = getattr(user, 'dept', None)
        if dept:
            result['dept_info'] = {
                'dept_id': dept.id,
                'dept_name': dept.name
            }
        role = getattr(user, 'role', None)
        if role:
            result['role_info'] = role.values('id', 'name', 'key')
        return DetailResponse(data=result, msg="获取成功")

    @action(methods=["PUT"], detail=False, permission_classes=[IsAuthenticated])
    def update_user_info(self, request):
        """修改当前用户信息"""
        serializer = UserInfoUpdateSerializer(request.user, data=request.data, request=request)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return DetailResponse(data=None, msg="修改成功")

    @action(methods=["PUT"], detail=True, permission_classes=[IsAuthenticated])
    def change_password(self, request, *args, **kwargs):
        """密码修改"""
        data = request.data
        old_pwd = data.get("oldPassword")
        new_pwd = data.get("newPassword")
        new_pwd2 = data.get("newPassword2")
        if old_pwd is None or new_pwd is None or new_pwd2 is None:
            return ErrorResponse(msg="参数不能为空")
        if new_pwd != new_pwd2:
            return ErrorResponse(msg="两次密码不匹配")
        check_password = request.user.check_password(old_pwd)
        if not check_password:
            check_password = request.user.check_password(hashlib.md5(old_pwd.encode(encoding='UTF-8')).hexdigest())
        if check_password:
            request.user.password = make_password(new_pwd)
            request.user.save()
            return DetailResponse(data=None, msg="修改成功")
        else:
            return ErrorResponse(msg="旧密码不正确")

    @action(methods=["PUT"], detail=True, permission_classes=[IsAuthenticated])
    def reset_to_default_password(self, request, *args, **kwargs):
        """恢复默认密码"""
        instance = Users.objects.filter(id=kwargs.get("pk")).first()
        if instance:
            instance.set_password(dispatch.get_system_config_values("base.default_password"))
            instance.save()
            return DetailResponse(data=None, msg="密码重置成功")
        else:
            return ErrorResponse(msg="未获取到用户")

    @action(methods=["PUT"], detail=True)
    def reset_password(self, request, pk):
        """
        密码重置
        """
        instance = Users.objects.filter(id=pk).first()
        data = request.data
        new_pwd = data.get("newPassword")
        new_pwd2 = data.get("newPassword2")
        if instance:
            if new_pwd != new_pwd2:
                return ErrorResponse(msg="两次密码不匹配")
            else:
                instance.password = make_password(new_pwd)
                instance.save()
                return DetailResponse(data=None, msg="修改成功")
        else:
            return ErrorResponse(msg="未获取到用户")
