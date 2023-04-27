
from django.db import models
from system.utils.models import CoreModel, table_prefix
import os
import hashlib


def media_file_name(instance, filename):
    h = instance.md5sum
    basename, ext = os.path.splitext(filename)
    return os.path.join("files", h[0:1], h[1:2], h + ext.lower())


class FileList(CoreModel):
    name = models.CharField(max_length=200, null=True, blank=True, verbose_name="名称", help_text="名称")
    url = models.FileField(upload_to=media_file_name)
    md5sum = models.CharField(max_length=36, blank=True, verbose_name="文件md5", help_text="文件md5")

    def save(self, *args, **kwargs):
        if not self.md5sum:  # file is new
            md5 = hashlib.md5()
            for chunk in self.url.chunks():
                md5.update(chunk)
            self.md5sum = md5.hexdigest()
        super(FileList, self).save(*args, **kwargs)

    class Meta:
        db_table = table_prefix + "system_file_list"
        verbose_name = "文件管理"
        verbose_name_plural = verbose_name
        ordering = ("-create_datetime",)
