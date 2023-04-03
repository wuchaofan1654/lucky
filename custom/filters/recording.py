import django_filters
from custom.models import Recording


class RecordingFilter(django_filters.rest_framework.FilterSet):
    """
    录制记录 简单序过滤器
    """
    unique_name = django_filters.CharFilter(lookup_expr='icontains')
    host = django_filters.CharFilter(lookup_expr='icontains')
    path = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Recording
        exclude = ('description', 'creator', 'modifier')
