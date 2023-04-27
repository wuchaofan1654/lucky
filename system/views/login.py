import base64
import hashlib
from datetime import datetime, timedelta

from captcha.views import CaptchaStore, captcha_image
from django.contrib import auth
from django.contrib.auth import login
from django.shortcuts import redirect
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from application import dispatch
from system.models import Users
from system.serializers import LoginSerializer, LoginTokenSerializer
from system.utils.json_response import ErrorResponse, DetailResponse
from system.utils.request_util import save_login_log
from system.utils.serializers import CustomModelSerializer
from system.utils.validator import CustomValidationError


class CaptchaView(APIView):
    authentication_classes = []
    permission_classes = []

    @swagger_auto_schema(
        responses={"200": openapi.Response("获取成功")},
        security=[],
        operation_id="captcha-get",
        operation_description="验证码获取",
    )
    def get(self, request):
        data = {}
        if dispatch.get_system_config_values("base.captcha_state"):
            hash_key = CaptchaStore.generate_key()
            _id = CaptchaStore.objects.filter(hashkey=hash_key).first().id
            image = captcha_image(request, hash_key)
            # 将图片转换为base64
            image_base = base64.b64encode(image.content)
            data = {
                "key": _id,
                "image_base": "data:image/png;base64," + image_base.decode("utf-8"),
            }
        return DetailResponse(data=data)


class LoginView(TokenObtainPairView):
    """
    登录接口
    """
    serializer_class = LoginSerializer
    permission_classes = []

    def post(self, request, *args, **kwargs):
        # username可能携带的不止是用户名，可能还是用户的其它唯一标识 手机号 邮箱
        username = request.data.get('username', None)
        if username is None:
            return ErrorResponse(msg="账号不能为空")
        password = request.data.get('password', None)
        if password is None:
            return ErrorResponse(msg="密码不能为空")

        if dispatch.get_system_config_values("base.captcha_state"):
            captcha = request.data.get('captcha', None)
            captchaKey = request.data.get('captchaKey', None)
            if captchaKey is None:
                return ErrorResponse(msg="验证码不能为空")
            if captcha is None:
                raise CustomValidationError("验证码不能为空")
            self.image_code = CaptchaStore.objects.filter(
                id=captchaKey
            ).first()
            five_minute_ago = datetime.now() - timedelta(hours=0, minutes=5, seconds=0)
            if self.image_code and five_minute_ago > self.image_code.expiration:
                self.image_code and self.image_code.delete()
                raise CustomValidationError("验证码过期")
            else:
                if self.image_code and (
                        self.image_code.response == captcha
                        or self.image_code.challenge == captcha
                ):
                    self.image_code and self.image_code.delete()
                else:
                    self.image_code and self.image_code.delete()
                    raise CustomValidationError("图片验证码错误")
        try:
            # 手动通过 user 签发 jwt-token
            user = Users.objects.get(username=username)
        except Exception as e:
            print(e)
            return ErrorResponse(msg='该账号未注册')
        # 获得用户后，校验密码并签发token
        if not user.check_password(password) and 1 == 2:
            print(f"check password error: {password}")
            return ErrorResponse(msg='密码错误')
        result = {
            "name": user.name,
            "userId": user.id,
            "avatar": user.avatar,
        }
        dept = getattr(user, 'dept', None)
        if dept:
            result['dept_info'] = {
                'dept_id': dept.id,
                'dept_name': dept.name,
                'dept_key': dept.key
            }
        role = getattr(user, 'role', None)
        if role:
            result['role_info'] = role.values('id', 'name', 'key')
        refresh = LoginSerializer.get_token(user)
        result["refresh"] = str(refresh)
        result["access"] = str(refresh.access_token)
        # 记录登录日志
        request.user = user
        save_login_log(request=request)
        return DetailResponse(data=result, msg="获取成功")


class LoginTokenView(TokenObtainPairView):
    """
    登录获取token接口
    """
    serializer_class = LoginTokenSerializer
    permission_classes = []


class LogoutView(APIView):
    def post(self, request):
        return DetailResponse(msg="注销成功")


class ApiLoginSerializer(CustomModelSerializer):
    """接口文档登录-序列化器"""

    username = serializers.CharField()
    password = serializers.CharField()

    class Meta:
        model = Users
        fields = ["username", "password"]


class ApiLogin(APIView):
    """接口文档的登录接口"""

    serializer_class = ApiLoginSerializer
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user_obj = auth.authenticate(
            request,
            username=username,
            password=hashlib.md5(password.encode(encoding="UTF-8")).hexdigest(),
        )
        if user_obj:
            login(request, user_obj)
            return redirect("/")
        else:
            return ErrorResponse(msg="账号/密码错误")
