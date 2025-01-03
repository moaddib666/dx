from rest_framework.routers import DefaultRouter

from apps.shields.api.views.openai import OpenAIActiveShieldsViewSet

OpenAIRouter = DefaultRouter()
OpenAIRouter.register('active', OpenAIActiveShieldsViewSet, basename='openai-shields')
