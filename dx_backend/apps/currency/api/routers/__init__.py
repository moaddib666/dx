from rest_framework.routers import DefaultRouter

from apps.currency.api.views.openai import OpenAIPlayerCurrencyTokensViewSet, OpenAIWorldCurrencyTokensViewSet

OpenAIRouter = DefaultRouter()
OpenAIRouter.register('player', OpenAIPlayerCurrencyTokensViewSet, basename='openai-player-currency-tokens')
OpenAIRouter.register('world', OpenAIWorldCurrencyTokensViewSet, basename='openai-world-currency-tokens')
