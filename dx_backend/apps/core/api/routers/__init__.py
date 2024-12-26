from rest_framework.routers import DefaultRouter

from apps.core.api.views.openai import CharacterStatsViewSet

OpenAIRouter = DefaultRouter()
OpenAIRouter.register('character/stats', CharacterStatsViewSet, basename='openai-character-stats')
# OpenAIRouter.register('world', OpenAIWorldCurrencyTokensViewSet, basename='openai-world-currency-tokens')
