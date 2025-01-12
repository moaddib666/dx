from rest_framework.routers import DefaultRouter

from apps.character.api.views.openai import OpenAISchoolsManagementViewSet, OpenAICharacterGameMasterManagementViewSet, \
    OpenAICharacterManageBaseStats

OpenAIRouter = DefaultRouter()
OpenAIRouter.register('player', OpenAISchoolsManagementViewSet, basename='openai')
OpenAIRouter.register('stats', OpenAICharacterManageBaseStats, basename='openai-stats')
OpenAIRouter.register('gm', OpenAICharacterGameMasterManagementViewSet, basename='openai-gm-character')
