# -*- coding: utf-8 -*-
"""
Create by sandy at 20:32 25/03/2022
Description: ToDo
"""

from rest_framework.routers import DefaultRouter

from custom.views import RecordingModelViewSet, CheckResultModelViewSet

router = DefaultRouter()
router.register(r'recording', RecordingModelViewSet)
router.register(r'check_result', CheckResultModelViewSet)

urlpatterns = []

urlpatterns += router.urls

