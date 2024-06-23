from rest_framework.routers import DefaultRouter

from ..views.openai import PlayerActionsViewSet


OpenAIRouter = DefaultRouter()
OpenAIRouter.register('', PlayerActionsViewSet, basename='openai-action ')
