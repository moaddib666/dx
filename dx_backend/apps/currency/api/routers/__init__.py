from rest_framework.routers import DefaultRouter

from apps.currency.api.views.openai import OpenAICharacterCurrencyTokensViewSet, OpenAIWorldCurrencyTokensViewSet

OpenAIRouter = DefaultRouter()
OpenAIRouter.register('character', OpenAICharacterCurrencyTokensViewSet, basename='openai-character-currency-tokens')
OpenAIRouter.register('world', OpenAIWorldCurrencyTokensViewSet, basename='openai-world-currency-tokens')
