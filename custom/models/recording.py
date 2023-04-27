from django.db.models import CharField, TextField

from system.utils.models import CoreModel


class Recording(CoreModel):
    host = CharField(
        default='',
        max_length=255,
        verbose_name='录制请求host',
        help_text='https://xxxx'
    )
    path = CharField(
        default='/',
        max_length=255,
        verbose_name='录制请求url',
        help_text='/xxxx'
    )
    unique_name = CharField(
        default='',
        max_length=255,
        verbose_name='录制记录唯一标识名称',
        help_text='host+url+request_meta加密',
    )
    request_meta = TextField(
        default=str,
        verbose_name='请求参数信息',
    )
    response_meta = TextField(
        default=str,
        verbose_name='请求响应信息',
    )

    class Meta:
        verbose_name = '录制记录'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.host}/{self.path}"
