from rest_framework.routers import DefaultRouter

from apps.effects.api.views.openai import OpenAIActiveEffectsViewSet

OpenAIRouter = DefaultRouter()
OpenAIRouter.register('active', OpenAIActiveEffectsViewSet, basename='openai-effects')
