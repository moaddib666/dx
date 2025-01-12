from rest_framework.routers import DefaultRouter

from apps.core.api.views.openai import CharacterStatsViewSet, ViolationViewSet, StatViewSet

OpenAIRouter = DefaultRouter()
OpenAIRouter.register('character/stats', CharacterStatsViewSet, basename='openai-character-stats')
OpenAIRouter.register('stats', StatViewSet, basename='openai-core-stats')
OpenAIRouter.register('violations', ViolationViewSet, basename='openai-core-violations')
