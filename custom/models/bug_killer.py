# coding=utf-8
"""
# Create by wuchaofan 
# At 2023/4/17
# Current Dir custom/models
"""

from system.utils.models import CoreModel
from django.db import models


class BugSet(CoreModel):
    title = models.CharField(
        verbose_name='BUG集合标题',
        max_length=120,
        default=''
    )
    desc = models.CharField(
        verbose_name='BUG集合描述',
        max_length=255,
        default=''
    )
    related_prd_id = models.CharField(
        default='',
        max_length=20,
        verbose_name='关联需求编号'
    )

    class Meta:
        verbose_name = 'BUG集合'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.title}"


class Bug(CoreModel):
    bug_set = models.ForeignKey(
        to="BugSet",
        verbose_name="BUG集合",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_constraint=False,
        help_text="关联BUG集合",
        related_name="Bug.bug_set+"
    )
    title = models.CharField(
        verbose_name='BUG标题',
        max_length=255,
        default=''
    )
    desc = models.CharField(
        verbose_name='BUG描述',
        max_length=255,
        default=''
    )
    level = models.IntegerField(
        verbose_name='BUG级别',
        default=2
    )
    solution = models.IntegerField(
        verbose_name='BUG解决方案',
        default=0
    )
    status = models.IntegerField(
        verbose_name='BUG状态',
        default=1
    )
    cause_reason = models.IntegerField(
        verbose_name='BUG原因',
        default=0
    )
    resource = models.CharField(
        verbose_name="附件📎",
        max_length=255,
        null=True,
        blank=True,
        default=''
    )
    follow_qa = models.ManyToManyField(
        to="system.Users",
        verbose_name="BUG跟进QA",
        db_constraint=False,
        help_text="BUG跟进QA",
        related_name="Bug.follow_QA+"
    )
    follow_rd = models.ManyToManyField(
        to="system.Users",
        verbose_name="跟进RD",
        db_constraint=False,
        help_text="BUG跟进RD",
        related_name="Bug.follow_RD+"
    )
    solve_datetime = models.DateTimeField(
        verbose_name='BUG解决时间',
        auto_created=True,
        auto_now=True
    )
    belong_rd = models.ForeignKey(
        to="system.Users",
        verbose_name="BUG归属RD",
        on_delete=models.PROTECT,
        db_constraint=False,
        null=True,
        blank=True,
        help_text="BUG归属RD",
        related_name="Bug.belong_RD+"
    )
    belong_dept = models.ForeignKey(
        to="system.Dept",
        verbose_name="BUG归属团队",
        on_delete=models.PROTECT,
        db_constraint=False,
        null=True,
        blank=True,
        help_text="BUG归属团队",
        related_name="Bug.belong_dept+"
    )
    close_qa = models.ForeignKey(
        to="system.Users",
        verbose_name="BUG关闭人",
        on_delete=models.PROTECT,
        db_constraint=False,
        null=True,
        blank=True,
        help_text="BUG关闭人",
        related_name="Bug.close_QA+"
    )
    close_datetime = models.DateTimeField(
        verbose_name='BUG关闭时间',
        auto_created=True,
        auto_now=True
    )

    class Meta:
        verbose_name = 'BUG管理'
        verbose_name_plural = verbose_name
        indexes = [models.Index(fields=['title', 'level', 'cause_reason'])]

    def __str__(self):
        return f"{self.title}"


class BugRecord(CoreModel):
    bug = models.ForeignKey(
        to="Bug",
        verbose_name="关联bug",
        on_delete=models.PROTECT,
        db_constraint=False,
        null=True,
        blank=True,
        help_text="关联bug",
        related_name="BugRecord.bug+"
    )
    content = models.CharField(
        verbose_name='操作内容',
        max_length=255,
        default=''
    )

    class Meta:
        verbose_name = 'BUG流转明细'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"{self.operator}-{self.content}"


