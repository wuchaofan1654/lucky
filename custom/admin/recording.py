from django.contrib import admin

# Register your models here.
from custom.models import Recording, CheckResult


admin.site.register(Recording)
admin.site.register(CheckResult)
