# -*- coding: utf-8 -*-
"""
Create by sandy at 20:32 25/03/2022
Description: ToDo
"""

from rest_framework.routers import DefaultRouter
from django.urls import path

from custom.views import RecordingModelViewSet, CheckResultModelViewSet, BugModelViewSet, \
    BugSetModelViewSet, BugRecordModelViewSet

router = DefaultRouter()
router.register(r'recording', RecordingModelViewSet)
router.register(r'check_result', CheckResultModelViewSet)
router.register(r'bug_set', BugSetModelViewSet)
router.register(r'bug', BugModelViewSet)
router.register(r'bug_record', BugRecordModelViewSet)

urlpatterns = [
    path(r'mitm/', RecordingModelViewSet.as_view({'get': 'push_message'})),
]

urlpatterns += router.urls

