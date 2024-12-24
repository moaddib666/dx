from rest_framework.routers import DefaultRouter

from apps.items.api.views.openai import OpenAICharacterItemsViewSet, WorldItemsViewSet

OpenAIRouter = DefaultRouter()
OpenAIRouter.register('character', OpenAICharacterItemsViewSet, basename='openai-character-items')
OpenAIRouter.register('world', WorldItemsViewSet, basename='openai-world-items')
