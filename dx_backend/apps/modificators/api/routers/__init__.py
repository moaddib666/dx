from rest_framework.routers import DefaultRouter

from apps.modificators.api.views.openai import OpenAIPlayerModificatorsViewSet, OpenAIWorldModificatorsViewSet

OpenAIRouter = DefaultRouter()
OpenAIRouter.register('player', OpenAIPlayerModificatorsViewSet, basename='openai-player-modificators')
OpenAIRouter.register('world', OpenAIWorldModificatorsViewSet, basename='openai-world-modificators')
