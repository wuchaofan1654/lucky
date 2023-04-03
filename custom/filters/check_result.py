import django_filters
from custom.models import CheckResult


class CheckResultFilter(django_filters.rest_framework.FilterSet):
    """
    检查结果 简单序过滤器
    """
    check_status = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = CheckResult
        exclude = ('description', 'creator', 'modifier')
