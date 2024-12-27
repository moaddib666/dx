from rest_framework.routers import DefaultRouter

from ..views.openai import CharacterActionsViewSet, CharacterActionsLogViewSet, GameMasterActionsViewSet

OpenAIRouter = DefaultRouter()
OpenAIRouter.register('', CharacterActionsViewSet, basename='openai-action ')
OpenAIRouter.register('log', CharacterActionsLogViewSet, basename='openai-action-log')

OpenAIRouter.register('gm', GameMasterActionsViewSet, basename='openai-action-gm')
