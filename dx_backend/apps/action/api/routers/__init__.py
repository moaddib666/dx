from rest_framework.routers import DefaultRouter

from ..views.openai import CharacterActionsViewSet


OpenAIRouter = DefaultRouter()
OpenAIRouter.register('', CharacterActionsViewSet, basename='openai-action ')
