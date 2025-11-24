from rest_framework.routers import DefaultRouter

from apps.character.api.views.openai import OpenAICharacterBaseManagementViewSet, OpenAICharacterGameMasterManagementViewSet, \
    OpenAICharacterManageBaseStats, ClientCharacterManagementViewSet, PublishedCharacterViewSet

OpenAIRouter = DefaultRouter()
OpenAIRouter.register('player', OpenAICharacterBaseManagementViewSet, basename='openai')
OpenAIRouter.register('stats', OpenAICharacterManageBaseStats, basename='openai-stats')
OpenAIRouter.register('gm', OpenAICharacterGameMasterManagementViewSet, basename='openai-gm-character')
OpenAIRouter.register('owned', ClientCharacterManagementViewSet, basename='characters')
OpenAIRouter.register('published', PublishedCharacterViewSet, basename='published-characters')
