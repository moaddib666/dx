from rest_framework.routers import DefaultRouter

from apps.character.api.views.openai import OpenAISchoolsManagementViewSet, OpenAICharacterGameMasterManagementViewSet, \
    OpenAICharacterManageBaseStats, ClientCharacterManagementViewSet

OpenAIRouter = DefaultRouter()
OpenAIRouter.register('', OpenAISchoolsManagementViewSet, basename='openai')
OpenAIRouter.register('stats', OpenAICharacterManageBaseStats, basename='openai-stats')
OpenAIRouter.register('gm', OpenAICharacterGameMasterManagementViewSet, basename='openai-gm-character')
OpenAIRouter.register('player/owned', ClientCharacterManagementViewSet, basename='client-characters')
