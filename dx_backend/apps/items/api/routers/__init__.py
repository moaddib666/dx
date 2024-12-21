from rest_framework.routers import DefaultRouter

from apps.items.api.views.openai import OpenAIPlayerItemsViewSet, WorldItemsViewSet

OpenAIRouter = DefaultRouter()
OpenAIRouter.register('player', OpenAIPlayerItemsViewSet, basename='openai-player-items')
OpenAIRouter.register('world', WorldItemsViewSet, basename='openai-world-items')
