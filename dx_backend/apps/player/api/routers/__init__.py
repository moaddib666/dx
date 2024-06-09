from rest_framework.routers import DefaultRouter

from apps.player.api.views.openai import OpenAICharacterManagementViewSet


OpenAIRouter = DefaultRouter()
OpenAIRouter.register(r'openapi', OpenAICharacterManagementViewSet, basename='openai')
