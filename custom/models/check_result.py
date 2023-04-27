from django.db.models import IntegerField, TextField

from system.utils.models import CoreModel


class CheckResult(CoreModel):
    related_id = IntegerField(
        default=0,
        verbose_name='结果关联实体id'
    )
    related_type = IntegerField(
        default=0,
        verbose_name='结果关联实体type'
    )
    result_status = IntegerField(
        default=0,
        verbose_name='比对结果'
    )
    result_message = TextField(
        default=str,
        verbose_name='比对结果信息'
    )

    class Meta:
        verbose_name = '检查结果'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.result_status}-{self.result_message}"


