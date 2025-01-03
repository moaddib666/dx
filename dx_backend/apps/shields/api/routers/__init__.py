from rest_framework.routers import DefaultRouter

from apps.shields.api.views.openai import OpenAIActiveShieldsViewSet, GameMasterOpenAIActiveShieldsViewSet

OpenAIRouter = DefaultRouter()
OpenAIRouter.register('active', OpenAIActiveShieldsViewSet, basename='openai-shields')
OpenAIRouter.register('gm/active', GameMasterOpenAIActiveShieldsViewSet, basename='openai-gm-shields')

