from rest_framework.routers import DefaultRouter

from apps.character.api.views.openai import OpenAISchoolsManagementViewSet, OpenAICharacterGameMasterManagementViewSet

OpenAIRouter = DefaultRouter()
OpenAIRouter.register('', OpenAISchoolsManagementViewSet, basename='openai')
OpenAIRouter.register('gm', OpenAICharacterGameMasterManagementViewSet, basename='openai-gm-character')
