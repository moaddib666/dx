from rest_framework.routers import DefaultRouter

from ..views.openai import CharacterActionsViewSet, CharacterActionsLogViewSet, GameMasterActionsViewSet, SpecialActionsViewSet

OpenAIRouter = DefaultRouter()
OpenAIRouter.register('', CharacterActionsViewSet, basename='openai-action ')
OpenAIRouter.register('log', CharacterActionsLogViewSet, basename='openai-action-log')
OpenAIRouter.register('special', SpecialActionsViewSet, basename='openai-action-special')

OpenAIRouter.register('gm', GameMasterActionsViewSet, basename='openai-action-gm')
